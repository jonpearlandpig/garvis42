"""
GARVIS Full Stack - System Configuration

Customize this file to rebrand your instance.
"""

SYSTEM_CONFIG = {
    # System Identity
    "name": "GOGARVIS",
    "tagline": "Sovereign Intelligence Framework",
    "version": "2.0.0",
    
    # Ownership
    "owner": "Pearl & Pig",
    "owner_id": "TSID-0001",
    "owner_url": "https://pearlandpig.com",
    
    # Visual Identity (defaults - can be overridden via Brand Profiles)
    "primary_color": "#FF4500",
    "secondary_color": "#1A1A1A",
    "font_heading": "JetBrains Mono",
    "font_body": "Manrope",
    
    # Feature Flags
    "features": {
        "ai_chat": True,
        "version_history": True,
        "audit_log": True,
        "google_auth": True,
    },
    
    # AI Configuration
    "ai": {
        "provider": "openai",
        "model": "gpt-5.2",
        "assistant_name": "GARVIS AI",
    },
    
    # Authority Hierarchy Labels (customize for your domain)
    "authority_layers": [
        {"id": "sovereign", "name": "SOVEREIGN AUTHORITY", "description": "Constitutional control"},
        {"id": "registry", "name": "TELAUTHORIUM", "description": "Rights & provenance"},
        {"id": "intelligence", "name": "GARVIS", "description": "Truth enforcement"},
        {"id": "phases", "name": "FLIGHTPATH COS", "description": "Phase discipline"},
        {"id": "routing", "name": "MOSE", "description": "Operator routing"},
        {"id": "operators", "name": "PIG PEN", "description": "AI operators"},
        {"id": "execution", "name": "TELA", "description": "Execution layer"},
        {"id": "audit", "name": "AUDIT LEDGER", "description": "Immutable log"},
    ],
    
    # Operator Categories (customize for your domain)
    "operator_categories": [
        "Core Resolution",
        "Business",
        "Creative",
        "Systems",
        "Quality",
        "Optional",
    ],
}

# AI System Prompt Template
SYSTEM_PROMPT_TEMPLATE = """You are {assistant_name}, the sovereign intelligence assistant for {system_name}.

You are knowledgeable about the system architecture, components, and governance framework.

Core Principles:
- Authority flows top to bottom
- No component can override one above it
- Execution only at the execution layer
- All actions logged to audit ledger

Respond in a professional, precise manner."""

def get_system_prompt():
    """Generate the AI system prompt from config"""
    return SYSTEM_PROMPT_TEMPLATE.format(
        assistant_name=SYSTEM_CONFIG["ai"]["assistant_name"],
        system_name=SYSTEM_CONFIG["name"],
    )
