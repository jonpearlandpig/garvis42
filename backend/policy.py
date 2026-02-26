# backend/policy.py
from typing import List, Dict, Optional
from pydantic import BaseModel
from datetime import datetime
import uuid
import hashlib
import json

# Assume models.py is in the same directory or accessible
from .models import AKB, AuditLog, AKBEntry, CACPolicy

# In-memory stores for PoC (swap to DB later)
AKB_STORE: Dict[str, AKB] = {}
AUDIT_LOG: List[AuditLog] = []
# In-memory store for CAC policies. Key: AKB ID, Value: CACPolicy
CAC_STORE: Dict[str, CACPolicy] = {}

# --- Audit Logging Helper ---
def append_audit_log_entry(entry_data: dict):
    # Add dynamic fields like ID, timestamp, checksum
    entry_data.setdefault("id", str(uuid.uuid4()))
    entry_data.setdefault("timestamp", datetime.utcnow())
    entry_data.setdefault("actor", "system") # Default actor
    entry_data.setdefault("confidence", None)
    entry_data.setdefault("source", None)

    # Ensure consistency for checksum calculation
    log_entry_dict = entry_data.copy()
    log_entry_dict["timestamp"] = log_entry_dict["timestamp"].isoformat() # Ensure serializable for hash

    # Calculate checksum for integrity
    checksum_data = json.dumps(log_entry_dict, sort_keys=True).encode()
    log_entry_dict["checksum"] = hashlib.sha256(checksum_data).hexdigest()

    try:
        # Use Pydantic model for validation and create dict for storage
        log_entry_model = AuditLog(**log_entry_dict)
        AUDIT_LOG.append(log_entry_model.dict())
    except Exception as e:
        print(f"Error validating and appending audit log: {e}")
        # Fallback: log raw dict if Pydantic fails, but this is risky.
        # For PoC, we might just skip if validation fails, or log the Pydantic error.

# --- Cross-AKB Access Control Logic ---
def get_cac_policy(akb_id: str) -> CACPolicy:
    """Retrieves CAC policy for an AKB, defaults to a restrictive policy."""
    return CAC_STORE.get(akb_id, CACPolicy(allowed_akb_ids=[], allow_cross_akb=False))

def can_access_akb(requesting_akb_id: str, target_akb_id: str) -> bool:
    """Checks if requesting_akb_id can access target_akb_id's data."""
    if requesting_akb_id == target_akb_id:
        return True # Accessing own AKB is always allowed

    policy = get_cac_policy(requesting_akb_id)

    if policy.allow_cross_akb and target_akb_id in policy.allowed_akb_ids:
        return True # Explicitly allowed by policy

    # Log denied access attempts and return False
    append_audit_log_entry({
         "akb_id": requesting_akb_id,
         "action": "cross_akb_access_denied",
         "detail": f"Denied access from {requesting_akb_id} to {target_akb_id}.",
         "source": "CAC_policy",
         "confidence": 1.0
    })
    return False

# --- Placeholder for future persistence ---
def initialize_stores():
    """Initializes in-memory stores. Placeholder for DB connection."""
    print("Initializing in-memory stores for PoC.")
    # In a real app, this would connect to databases (SQLite, Postgres, MongoDB)
    # and load existing data.
    pass

def save_akb_to_store(akb: AKB):
    AKB_STORE[akb.id] = akb
    CAC_STORE[akb.id] = get_cac_policy(akb.id) # Ensure policy is loaded/initialized if it's new

def get_akb_from_store(akb_id: str) -> Optional[AKB]:
    return AKB_STORE.get(akb_id)
