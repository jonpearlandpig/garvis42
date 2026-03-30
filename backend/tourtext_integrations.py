"""
TourText Emergent - External Integrations
Twilio SMS, OpenAI NLP, Supabase storage.

Constraint (enforced in code and docs):
  LLM handles: intent parsing, answer formatting, natural language generation
  LLM NEVER decides: truth, finance, conflict resolution
"""
import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Twilio SMS
# ---------------------------------------------------------------------------

class TwilioSMS:
    """Thin wrapper around the Twilio REST API for outbound SMS."""

    def __init__(self):
        self.account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
        self.auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
        self.from_number = os.environ.get("TWILIO_PHONE_NUMBER")
        self._client = None

    def _get_client(self):
        if self._client is None:
            try:
                from twilio.rest import Client
                self._client = Client(self.account_sid, self.auth_token)
            except ImportError:
                logger.warning("twilio package not installed — SMS disabled")
            except Exception as exc:
                logger.warning("Twilio init failed: %s", exc)
        return self._client

    async def send_sms(self, to: str, body: str) -> Dict[str, Any]:
        client = self._get_client()
        if not client:
            return {"success": False, "error": "Twilio unavailable"}
        try:
            message = client.messages.create(body=body, from_=self.from_number, to=to)
            return {"success": True, "sid": message.sid, "status": message.status}
        except Exception as exc:
            logger.error("SMS send failed: %s", exc)
            return {"success": False, "error": str(exc)}


# ---------------------------------------------------------------------------
# OpenAI NLP processor
# ---------------------------------------------------------------------------

class OpenAIProcessor:
    """
    GPT integration for intent parsing and response formatting ONLY.

    Constraint: the LLM is never the source of truth — it only parses and
    formats.  All truth decisions are made by deterministic retrieval logic.
    """

    def __init__(self):
        self.api_key = os.environ.get("OPENAI_API_KEY")
        self._client = None

    def _get_client(self):
        if self._client is None:
            try:
                from openai import AsyncOpenAI
                self._client = AsyncOpenAI(api_key=self.api_key)
            except ImportError:
                logger.warning("openai package not installed — NLP degraded to basic mode")
            except Exception as exc:
                logger.warning("OpenAI init failed: %s", exc)
        return self._client

    async def parse_intent(self, query: str) -> Dict[str, Any]:
        """Extract intent and keywords from a natural-language crew query."""
        client = self._get_client()
        if not client:
            return self._basic_intent(query)
        try:
            response = await client.chat.completions.create(
                model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a tour information assistant that parses crew queries. "
                            "Extract: intent (show_info|venue_info|contact|finance|safety|general), "
                            "keywords (list of relevant terms), confidence (0-1). "
                            "Respond with JSON only."
                        ),
                    },
                    {"role": "user", "content": query},
                ],
                temperature=0.1,
                max_tokens=200,
                response_format={"type": "json_object"},
            )
            import json
            return json.loads(response.choices[0].message.content)
        except Exception as exc:
            logger.warning("Intent parse failed, using basic: %s", exc)
            return self._basic_intent(query)

    async def format_response(self, query: str, truth_records: List[Dict], context: str = "") -> str:
        """Format truth records into a natural-language SMS-safe response."""
        client = self._get_client()
        if not client or not truth_records:
            return self._basic_format(truth_records)
        try:
            records_text = "\n".join(
                f"- {r.get('record_type', 'info')}: {r.get('content', '')}"
                for r in truth_records[:5]
            )
            response = await client.chat.completions.create(
                model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a tour information assistant. "
                            "Format the provided verified data into a concise SMS response (max 160 chars). "
                            "Do NOT add information not present in the data. "
                            "Never make financial decisions."
                        ),
                    },
                    {
                        "role": "user",
                        "content": f"Query: {query}\n\nVerified data:\n{records_text}",
                    },
                ],
                temperature=0.2,
                max_tokens=100,
            )
            return response.choices[0].message.content.strip()
        except Exception as exc:
            logger.warning("Format response failed, using basic: %s", exc)
            return self._basic_format(truth_records)

    def _basic_intent(self, query: str) -> Dict[str, Any]:
        query_lower = query.lower()
        if any(w in query_lower for w in ["show", "gig", "date", "when", "setlist"]):
            intent = "show_info"
        elif any(w in query_lower for w in ["venue", "where", "address", "load"]):
            intent = "venue_info"
        elif any(w in query_lower for w in ["contact", "who", "phone", "email"]):
            intent = "contact"
        elif any(w in query_lower for w in ["payment", "settlement", "money", "fee"]):
            intent = "finance"
        elif any(w in query_lower for w in ["safety", "emergency", "medical"]):
            intent = "safety"
        else:
            intent = "general"
        words = [w for w in query_lower.split() if len(w) > 2]
        return {"intent": intent, "keywords": words[:10], "confidence": 0.6}

    def _basic_format(self, truth_records: List[Dict]) -> str:
        if not truth_records:
            return "No information found for your query."
        record = truth_records[0]
        content = record.get("content", "")
        if isinstance(content, dict):
            parts = [f"{k}: {v}" for k, v in list(content.items())[:4]]
            return " | ".join(parts)
        return str(content)[:160]


# ---------------------------------------------------------------------------
# Supabase / local file storage
# ---------------------------------------------------------------------------

class SupabaseStorage:
    """Upload files to Supabase; falls back to local /tmp storage."""

    LOCAL_DIR = Path("/tmp/tourtext_files")

    def __init__(self):
        self.url = os.environ.get("SUPABASE_URL")
        self.key = os.environ.get("SUPABASE_KEY")
        self.bucket = os.environ.get("SUPABASE_BUCKET", "tourtext-files")
        self._client = None

    def _get_client(self):
        if self._client is None:
            try:
                from supabase import create_client
                self._client = create_client(self.url, self.key)
            except Exception:
                pass
        return self._client

    async def upload(self, filename: str, content: bytes) -> Dict[str, Any]:
        client = self._get_client()
        if client:
            try:
                res = client.storage.from_(self.bucket).upload(filename, content)
                return {"success": True, "path": filename, "provider": "supabase"}
            except Exception as exc:
                logger.warning("Supabase upload failed, using local: %s", exc)
        return self._local_save(filename, content)

    def _local_save(self, filename: str, content: bytes) -> Dict[str, Any]:
        self.LOCAL_DIR.mkdir(parents=True, exist_ok=True)
        dest = self.LOCAL_DIR / filename
        dest.write_bytes(content)
        return {"success": True, "path": str(dest), "provider": "local"}


# ---------------------------------------------------------------------------
# Module-level singletons
# ---------------------------------------------------------------------------
twilio_client = TwilioSMS()
openai_processor = OpenAIProcessor()
supabase_storage = SupabaseStorage()
