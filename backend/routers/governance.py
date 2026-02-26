# backend/routers/governance.py
from fastapi import APIRouter, HTTPException, Query, Body, Depends
from pydantic import BaseModel as PydanticBaseModel
from typing import List, Dict, Optional, Any
from datetime import datetime
import uuid
import random

from ..models import AKB, AKBEntry, AuditLog, CACPolicy
from ..policy import AKB_STORE, AUDIT_LOG, CAC_STORE, can_access_akb, get_cac_policy, append_audit_log_entry, save_akb_to_store, get_akb_from_store
from ..llm_adapters import LLM_DISPATCHER

router = APIRouter(prefix="/governance", tags=["Governance"])

class EvaluateRequest(PydanticBaseModel):
    akb_id: str
    action: str

class GenerateDocRequest(PydanticBaseModel):
    akb_id: str
    approve: bool = False
    llm_adapter_key: str = Body("openai_like", description="Key of the LLM adapter to use (e.g., 'openai_like', 'local_mock'). Defaults to 'openai_like'.")

class DocResult(PydanticBaseModel):
    ok: bool
    content: str = ""
    explainability: str = ""
    generated_at: datetime = None

class AuditExportResponse(PydanticBaseModel):
    format: str
    data: str

@router.post("/akb", response_model=AKB)
def create_akb(payload: Dict[str, Any]):
    now = datetime.utcnow()
    akb_id = str(uuid.uuid4())
    akb = AKB(id=akb_id, name=payload["name"], owner=payload["owner"], created_at=now, updated_at=now, entries=[])
    save_akb_to_store(akb)
    CAC_STORE[akb_id] = CACPolicy(allowed_akb_ids=[], allow_cross_akb=False)
    append_audit_log_entry({
        "akb_id": akb_id,
        "action": "create_akb",
        "detail": f"AKB '{payload['name']}' created by owner '{payload['owner']}'.",
        "source": "api_call",
        "confidence": 1.0
    })
    return akb

@router.get("/akb/{akb_id}", response_model=AKB)
def get_akb(akb_id: str):
    akb = get_akb_from_store(akb_id)
    if not akb:
        raise HTTPException(404, "AKB not found.")
    return akb

@router.post("/akb/{akb_id}/evaluate", response_model=Dict[str, Any])
def evaluate_action(akb_id: str, payload: EvaluateRequest):
    akb = get_akb_from_store(akb_id)
    if not akb:
        raise HTTPException(404, "AKB not found.")
    allowed = False
    detail = "Action not permitted by current policy."
    confidence = 0.5
    source = "policy_engine"
    if payload.action == "read":
        allowed = True
        detail = "Read action allowed by default."
        confidence = 1.0
    append_audit_log_entry({
        "akb_id": akb_id,
        "action": "evaluate_action",
        "detail": f"Action '{payload.action}' evaluation: {detail}",
        "actor": payload.action.split('_')[0] if payload.action else 'user',
        "source": source,
        "confidence": confidence
    })
    return {"akb_id": akb_id, "action": payload.action, "allowed": allowed, "detail": detail}

@router.post("/akb/{akb_id}/request-action", response_model=Dict[str, Any])
def request_action(akb_id: str, payload: GenerateDocRequest):
    akb = get_akb_from_store(akb_id)
    if not akb:
        raise HTTPException(404, "AKB not found.")
    action_to_perform = "generate_doc"
    GATED_ACTIONS = ["generate_doc", "export_data", "delete_akb"]
    if action_to_perform in GATED_ACTIONS and not payload.approve:
        audit_detail = f"Action '{action_to_perform}' by {akb.owner} requested, requires human approval."
        append_audit_log_entry({
             "akb_id": akb_id,
             "action": f"request_{action_to_perform}",
             "actor": akb.owner,
             "detail": audit_detail,
             "source": "user_request",
             "confidence": 0.7
        })
        return {"status": "pending_approval", "message": "Human approval required.", "action_requested": action_to_perform}
    if action_to_perform == "generate_doc":
        return generate_doc_implementation(akb_id)
    raise HTTPException(501, "Action not implemented.")

def generate_doc_implementation(akb_id: str) -> Dict[str, Any]:
    akb = get_akb_from_store(akb_id)
    if not akb: raise HTTPException(404, "AKB not found.")
    linked_akb_check_allowed = True
    linked_akb_details = []
    if akb.linked_akbs:
        for linked_id in akb.linked_akbs:
            if can_access_akb(akb_id, linked_id):
                linked_akb_details.append(f"AKB {linked_id} (Allowed)")
            else:
                linked_akb_check_allowed = False
                linked_akb_details.append(f"AKB {linked_id} (Denied)")
                append_audit_log_entry({
                     "akb_id": akb_id,
                     "action": "cross_akb_access_check",
                     "detail": f"Attempted to access linked AKB {linked_id}, denied by CAC policy.",
                     "source": "CAC_policy",
                     "confidence": 0.0
                })
    context_for_llm = {
        "sources": [f"AKB:{akb.id}"],
        "linked_akbs_access": ", ".join(linked_akb_details) if akb.linked_akbs else "None",
        "akb_entries_count": len(akb.entries)
    }
    prompt = f"Generate a descriptive document summarising AKB '{akb.name}' by owner '{akb.owner}'. Context: {context_for_llm}"
    try:
        resp_openai = LLM_DISPATCHER.generate(prompt, context_data={**context_for_llm, "sources": context_for_llm["sources"] + ["openai_data"]})
        resp_mock = LLM_DISPATCHER.generate(prompt, context_data={**context_for_llm, "sources": context_for_llm["sources"] + ["mock_data"]})
        generated_text = f"--- Document for AKB: {akb.name} ---\n"
        generated_text += f"Owner: {akb.owner}\n"
        generated_text += f"Entries Count: {len(akb.entries)}\n"
        generated_text += f"Created: {akb.created_at.isoformat()}\n"
        generated_text += "\n--- AI Content (OpenAI-like) ---\n"
        generated_text += resp_openai.get("text", "N/A")
        generated_text += f"\n(Sources: {', '.join(resp_openai.get('sources', []))}, Confidence: {resp_openai.get('confidence', 0.0):.2f})"
        generated_text += "\n\n--- AI Content (Local Mock) ---\n"
        generated_text += resp_mock.get("text", "N/A")
        generated_text += f"\n(Sources: {', '.join(resp_mock.get('sources', []))}, Confidence: {resp_mock.get('confidence', 0.0):.2f})"
        explainability = (
            f"Generated using dual LLMs ({LLM_DISPATCHER.adapters['openai_like'].name}, "
            f"{LLM_DISPATCHER.adapters['local_mock'].name}). "
            f"Primary sources: {', '.join(context_for_llm['sources'])}. "
            f"Linked AKB access: {context_for_llm['linked_akbs_access']}. "
            f"Overall confidence derived from LLM outputs."
        )
        append_audit_log_entry({
            "akb_id": akb_id,
            "action": "generate_doc",
            "detail": f"Document generated for AKB '{akb.name}'.",
            "actor": akb.owner,
            "source": "dual_llm_orchestration",
            "confidence": (resp_openai.get("confidence", 0.0) + resp_mock.get("confidence", 0.0)) / 2
        })
        return {"ok": True, "content": generated_text, "explainability": explainability, "generated_at": datetime.utcnow()}
    except Exception as e:
        print(f"Error generating doc: {e}")
        append_audit_log_entry({
            "akb_id": akb_id,
            "action": "generate_doc_error",
            "detail": f"Failed to generate document: {str(e)}",
            "actor": akb.owner,
            "source": "llm_error",
            "confidence": 0.0
        })
        raise HTTPException(500, f"Failed to generate document: {str(e)}")

@router.get("/audit/export")
def export_audit(format: str = Query("json", enum=["json", "csv"])):
    if not AUDIT_LOG:
        return {"message": "No audit logs found."}
    if format == "json":
        response_data = [log for log in AUDIT_LOG]
        return {"format": "json", "data": response_data}
    elif format == "csv":
        import csv
        import io
        output = io.StringIO()
        fieldnames = list(AUDIT_LOG[0].keys()) if AUDIT_LOG else []
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        for log_entry in AUDIT_LOG:
            writer.writerow(log_entry)
        return {"format": "csv", "data": output.getvalue()}
    raise HTTPException(400, "Unsupported format. Use 'json' or 'csv'.")

@router.get("/adapters/available")
def get_available_adapters():
    return LLM_DISPATCHER.get_available_adapters()

@router.post("/adapters/set_current")
def set_current_adapter(adapter_key: str = Body(...)):
    if adapter_key not in LLM_DISPATCHER.adapters:
        raise HTTPException(400, f"Adapter '{adapter_key}' not found. Available: {list(LLM_DISPATCHER.adapters.keys())}")
    LLM_DISPATCHER.set_adapter(adapter_key)
    append_audit_log_entry({
        "action": "set_llm_adapter",
        "detail": f"LLM adapter set to: '{adapter_key}'.",
        "actor": "user",
        "source": "runtime_config",
        "confidence": 1.0
    })
    return {"message": f"LLM adapter set to '{adapter_key}'."}
