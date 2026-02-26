
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class AKBEntry(BaseModel):
    key: str
    value: str
    source: str = Field(..., description="Identifier for the source of this data (e.g., file path, external API endpoint, LLM call ID).")
    source_type: str = Field("manual", description="Type of source (manual, api, llm, import).")
    confidence: float = Field(1.0, description="Confidence score (0.0-1.0) for AI-generated data.")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when this entry was created.")
    version: int = Field(1, description="Version number for this entry.")

class CACPolicy(BaseModel):
    """Cross-AKB Access Control Policy."""
    allowed_akb_ids: List[str] = Field(default_factory=list, description="List of AKB IDs this policy explicitly allows cross-access to.")
    allow_cross_akb: bool = Field(False, description="If true, allows access to any AKB (use with extreme caution).")
    # Placeholder for more complex policy rules in the future
    # policy_name: str = "default_cac_policy" # Placeholder for renaming

class AKB(BaseModel):
    id: str = Field(..., description="Unique identifier for the AKB.")
    name: str = Field(..., description="Human-readable name for the AKB.")
    owner: str = Field(..., description="Owner of the AKB (e.g., user ID or organization name).")
    entries: List[AKBEntry] = Field(default_factory=list, description="Data entries within this AKB.")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when the AKB was created.")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when the AKB was last updated.")
    linked_akbs: List[str] = Field(default_factory=list, description="List of AKB IDs this AKB is explicitly linked to for potential access.")

class AuditLog(BaseModel):
    id: str = Field(..., description="Unique ID of the audit log entry.")
    akb_id: str = Field(..., description="The AKB associated with this action.")
    action: str = Field(..., description="The action performed (e.g., 'create_akb', 'evaluate', 'generate_doc').")
    actor: str = Field("system", description="Actor performing the action (user ID, system, AI model).")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of the action.")
    detail: str = Field(..., description="Specific details of the action, including outcome.")
    source: Optional[str] = Field(None, description="The source of the data or decision leading to this action.")
    confidence: Optional[float] = Field(None, description="Confidence score associated with the action, especially if AI-driven.")
    checksum: Optional[str] = Field(None, description="Hash of the log entry for integrity verification.")
