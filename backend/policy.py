# backend/policy.py
from typing import List, Dict, Optional
from pydantic import BaseModel as PydanticBaseModel, Field
from datetime import datetime
import uuid
import hashlib
import json

from .models import AKB, AuditLog, CACPolicy, AKBEntry
from .persistence import PersistenceLayer, get_persistence_layer

AKB_STORE: Dict[str, AKB] = {}
CAC_STORE: Dict[str, CACPolicy] = {}
AUDIT_LOG: List[AuditLog] = []

def append_audit_log_entry(entry_data: dict):
    entry_data.setdefault("id", str(uuid.uuid4()))
    entry_data.setdefault("timestamp", datetime.utcnow())
    entry_data.setdefault("actor", "system")
    entry_data.setdefault("confidence", None)
    entry_data.setdefault("source", None)
    log_entry_dict = entry_data.copy()
    log_entry_dict["timestamp"] = log_entry_dict["timestamp"].isoformat()
    checksum_data = json.dumps(log_entry_dict, sort_keys=True).encode()
    log_entry_dict["checksum"] = hashlib.sha256(checksum_data).hexdigest()
    try:
        log_entry_model = AuditLog(**log_entry_dict)
        AUDIT_LOG.append(log_entry_model)
        persistence = get_persistence_layer()
        persistence.append_audit(log_entry_model.dict())
    except Exception as e:
        print(f"Error validating and appending audit log: {e}")

def get_cac_policy(akb_id: str) -> CACPolicy:
    return CAC_STORE.get(akb_id, CACPolicy())

def can_access_akb(requesting_akb_id: str, target_akb_id: str) -> bool:
    if requesting_akb_id == target_akb_id:
        return True
    policy = get_cac_policy(requesting_akb_id)
    if policy.allow_cross_akb and target_akb_id in policy.allowed_akb_ids:
        return True
    append_audit_log_entry({
        "akb_id": requesting_akb_id,
        "action": "cross_akb_access_denied",
        "actor": "system",
        "detail": f"Denied access from AKB '{requesting_akb_id}' to AKB '{target_akb_id}'.",
        "source": "CAC_policy",
        "confidence": 1.0
    })
    return False

def initialize_stores():
    print("Initializing global stores from persistence...")
    persistence = get_persistence_layer()
    try:
        all_akbs = persistence.get_all_akbs()
        for akb in all_akbs:
            AKB_STORE[akb.id] = akb
            cac_policy = persistence.get_cac_policy_for_akb(akb.id)
            CAC_STORE[akb.id] = cac_policy if cac_policy else CACPolicy()
        print(f"Loaded {len(AKB_STORE)} AKBs, {len(CAC_STORE)} CAC policies.")
    except Exception as e:
        print(f"Error initializing stores from persistence: {e}")

def save_akb_to_store(akb: AKB):
    AKB_STORE[akb.id] = akb
    CAC_STORE[akb.id] = get_cac_policy(akb.id)
    persistence = get_persistence_layer()
    persistence.save_akb(akb)

def get_akb_from_store(akb_id: str) -> Optional[AKB]:
    if akb_id in AKB_STORE:
        return AKB_STORE[akb_id]
    persistence = get_persistence_layer()
    akb_from_db = persistence.get_akb(akb_id)
    if akb_from_db:
        AKB_STORE[akb_id] = akb_from_db
        if akb_id not in CAC_STORE:
            cac_policy = persistence.get_cac_policy_for_akb(akb_id)
            CAC_STORE[akb_id] = cac_policy if cac_policy else CACPolicy()
        return akb_from_db
    return None
