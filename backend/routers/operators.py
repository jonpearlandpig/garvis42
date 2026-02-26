from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from fastapi.responses import StreamingResponse
from pypdf2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from docx import Document
from openpyxl import Workbook, load_workbook
from io import BytesIO

router = APIRouter(prefix="/api/operators", tags=["Operators"])

@router.post("/dochandler")
async def doc_handler(
    action: str = Form(...),  # "create", "read", "edit"
    file_type: str = Form(...),  # "pdf", "docx", "xlsx"
    file: UploadFile = File(None),  # Optional for create
    content: str = Form(None)  # For create/edit
):
    if action == "create":
        if file_type == "pdf":
            buffer = BytesIO()
            c = canvas.Canvas(buffer)
            c.drawString(100, 100, content or "Test PDF")
            c.save()
            buffer.seek(0)
            return StreamingResponse(buffer, media_type="application/pdf")
        elif file_type == "docx":
            buffer = BytesIO()
            doc = Document()
            doc.add_paragraph(content or "Test DOCX")
            doc.save(buffer)
            buffer.seek(0)
            return StreamingResponse(buffer, media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        elif file_type == "xlsx":
            buffer = BytesIO()
            wb = Workbook()
            ws = wb.active
            ws["A1"] = content or "Test XLSX"
            wb.save(buffer)
            buffer.seek(0)
            return StreamingResponse(buffer, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    # Add read/edit logic similarly using the libraries

# Subagent spawning endpoint
@router.post("/spawn")
async def spawn_subagent(task: str = Form(...), operator: str = Form(...)):
    # Simulate task queueing and audit logging
    subagent_id = f"subagent-{operator}-{task}"
    # TODO: Integrate with real queue/audit
    return {
        "status": "queued",
        "subagent_id": subagent_id,
        "operator": operator,
        "task": task,
        "audit": {"action": "spawn", "operator": operator, "task": task}
    }
