"""
TourText Emergent - Utility Functions
TAID generation, phone/file hashing, tour code generation
"""
import hashlib
import random
import re
import string
import uuid
from datetime import datetime


def generate_taid(prefix: str = "TT") -> str:
    """Generate a Telauthorium Audit Identifier in format TAID-{PREFIX}-XXXXX"""
    suffix = "".join(random.choices(string.ascii_uppercase + string.digits, k=5))
    return f"TAID-{prefix}-{suffix}"


def generate_tour_taid() -> str:
    return generate_taid("TT-TOUR")


def generate_src_taid() -> str:
    return generate_taid("TT-SRC")


def generate_rec_taid() -> str:
    return generate_taid("TT-REC")


def generate_inv_taid() -> str:
    return generate_taid("TT-INV")


def generate_tkt_taid() -> str:
    return generate_taid("TT-TKT")


def generate_uuid() -> str:
    return str(uuid.uuid4())


def hash_phone_number(phone: str) -> str:
    """Hash phone number for privacy — never store raw phone numbers in logs."""
    return hashlib.sha256(phone.strip().encode()).hexdigest()


def hash_file(content: bytes) -> str:
    """SHA256 checksum of file bytes for deduplication."""
    return hashlib.sha256(content).hexdigest()


def generate_tour_code(name: str) -> str:
    """Derive an abbreviated tour code from the tour name.

    Takes the initial letter of each word (max 4 chars) and appends the last
    two digits of any 4-digit year found in the name.  Falls back to 'TOUR'.
    """
    words = name.strip().split()
    initials = "".join(w[0].upper() for w in words if w)[:4]
    year_match = re.search(r"\b(\d{4})\b", name)
    year_suffix = year_match.group(1)[-2:] if year_match else str(datetime.utcnow().year)[-2:]
    return (initials + year_suffix) if initials else "TOUR"
