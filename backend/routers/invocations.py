from fastapi import APIRouter
from datetime import datetime

router = APIRouter(prefix="/api/invocations", tags=["Invocations"])

# Dummy recent invocation traces
RECENT_TRACES = [
    {
        "domain": "finance",
        "trigger": "user_request",
        "operator_scores": {"Alice": 0.95, "Bob": 0.87},
        "provider": "OpenAI",
        "timeline": [
            {"event": "start", "timestamp": datetime.now().isoformat()},
            {"event": "decision", "timestamp": datetime.now().isoformat()},
            {"event": "complete", "timestamp": datetime.now().isoformat()},
        ]
    },
    {
        "domain": "legal",
        "trigger": "auto_audit",
        "operator_scores": {"Carol": 0.92, "David": 0.81},
        "provider": "Anthropic",
        "timeline": [
            {"event": "start", "timestamp": datetime.now().isoformat()},
            {"event": "decision", "timestamp": datetime.now().isoformat()},
            {"event": "complete", "timestamp": datetime.now().isoformat()},
        ]
    }
]

@router.get("/recent")
def get_recent_invocations():
    return RECENT_TRACES
