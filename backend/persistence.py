# backend/persistence.py
# This file is a blueprint for future persistence layer (e.g., SQLite, PostgreSQL)
# For the PoC, it's not used directly.

import sqlite3
from typing import List, Dict, Optional
from .models import AKB, AuditLog, CACPolicy, AKBEntry

class PersistenceLayer:
    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self.conn = None

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row # Return rows as dict-like objects
            self._create_tables()
            print(f"Connected to persistence layer: {self.db_path}")
        except Exception as e:
            print(f"Error connecting to database: {e}")
            raise

    def _create_tables(self):
        if not self.conn: return
        cursor = self.conn.cursor()
        # AKB Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS akbs (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                owner TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
        # AKB Entries Table (to store complex JSON/BLOB)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS akb_entries (
                id TEXT PRIMARY KEY,
                akb_id TEXT NOT NULL,
                key TEXT NOT NULL,
                value TEXT, -- Store as JSON string or TEXT
                source TEXT,
                source_type TEXT,
                confidence REAL,
                created_at TEXT,
                version INTEGER,
                FOREIGN KEY (akb_id) REFERENCES akbs(id)
            )
        """)
        # CAC Policy Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cac_policies (
                akb_id TEXT PRIMARY KEY,
                allowed_akb_ids TEXT, -- Store as JSON array string
                allow_cross_akb BOOLEAN,
                FOREIGN KEY (akb_id) REFERENCES akbs(id)
            )
        """)
        # Audit Log Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_log (
                id TEXT PRIMARY KEY,
                akb_id TEXT,
                action TEXT NOT NULL,
                actor TEXT,
                timestamp TEXT NOT NULL,
                detail TEXT,
                source TEXT,
                confidence REAL,
                checksum TEXT
            )
        """)
        self.conn.commit()

    def save_akb(self, akb: AKB):
        if not self.conn: raise RuntimeError("Database not connected.")
        cursor = self.conn.cursor()

        # Save main AKB data
        cursor.execute("""
            INSERT OR REPLACE INTO akbs (id, name, owner, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)
        """, (akb.id, akb.name, akb.owner, akb.created_at.isoformat(), akb.updated_at.isoformat()))

        # Save/Update entries (handle entry versions/updates carefully)
        cursor.execute("DELETE FROM akb_entries WHERE akb_id = ?", (akb.id,)) # Simple clear & re-add for MVP
        for entry in akb.entries:
            cursor.execute("""
                INSERT INTO akb_entries (id, akb_id, key, value, source, source_type, confidence, created_at, version)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (str(uuid.uuid4()), akb.id, entry.key, entry.value, entry.source, entry.source_type, entry.confidence, entry.created_at.isoformat(), entry.version))

        # Save CAC policy
        cac_policy = CAC_STORE.get(akb.id) # Assuming CAC_STORE reflects current policies
        if cac_policy:
            cursor.execute("""
                INSERT OR REPLACE INTO cac_policies (akb_id, allowed_akb_ids, allow_cross_akb)
                VALUES (?, ?, ?)
            """, (akb.id, json.dumps(cac_policy.allowed_akb_ids), cac_policy.allow_cross_akb))

        self.conn.commit()

    def get_akb(self, akb_id: str) -> Optional[AKB]:
        if not self.conn: raise RuntimeError("Database not connected.")
        cursor = self.conn.cursor()

        cursor.execute("SELECT * FROM akbs WHERE id = ?", (akb_id,))
        akb_row = cursor.fetchone()
        if not akb_row: return None

        akb_data = dict(akb_row)
        akb_data['created_at'] = datetime.fromisoformat(akb_data['created_at'])
        akb_data['updated_at'] = datetime.fromisoformat(akb_data['updated_at'])

        # Load entries
        cursor.execute("SELECT * FROM akb_entries WHERE akb_id = ?", (akb_id,))
        entries_rows = cursor.fetchall()
        akb_data['entries'] = []
        if entries_rows:
            for entry_row in entries_rows:
                entry_data = dict(entry_row)
                entry_data['created_at'] = datetime.fromisoformat(entry_data['created_at'])
                akb_data['entries'].append(AKBEntry(**entry_data))

        # Load CAC policy
        cursor.execute("SELECT * FROM cac_policies WHERE akb_id = ?", (akb_id,))
        policy_row = cursor.fetchone()
        if policy_row:
            cac_data = dict(policy_row)
            cac_data['allowed_akb_ids'] = json.loads(cac_data.get('allowed_akb_ids', '[]'))
            cac_policy = CACPolicy(**cac_data)
            CAC_STORE[akb_id] = cac_policy # Update global store
            akb_data['cac_policy'] = cac_policy

        return AKB(**akb_data)

    def append_audit(self, entry_data: dict):
        if not self.conn: raise RuntimeError("Database not connected.")
        # Audit log is generally append-only and very simple inserts
        # This function assumes entry_data is already formatted (e.g. has id, timestamp, detail, etc.)
        # and validated by Pydantic in the main router.
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO audit_log (id, akb_id, action, actor, timestamp, detail, source, confidence, checksum)
                VALUES (:id, :akb_id, :action, :actor, :timestamp, :detail, :source, :confidence, :checksum)
            """, entry_data)
            self.conn.commit()
        except Exception as e:
            print(f"Error writing to audit log: {e}")

    def get_audit_logs(self) -> List[Dict]:
        if not self.conn: raise RuntimeError("Database not connected.")
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM audit_log ORDER BY timestamp DESC")
        return [dict(row) for row in cursor.fetchall()]

    def close(self):
        if self.conn:
            self.conn.close()
            print("Persistence layer connection closed.")

# Global instance (will default to in-memory for PoC)
PERSISTENCE = PersistenceLayer(db_path=":memory:") # ':memory:' for in-memory; 'audits.db' for SQLite file

def get_persistence_layer():
    """Dependency injection for persistence layer."""
    # In a real app, you might handle connection pooling and ensure it's initialized
    if not PERSISTENCE.conn:
        PERSISTENCE.connect()
    return PERSISTENCE
