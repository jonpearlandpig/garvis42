# Customization Guide

This guide explains how to customize GARVIS Full Stack for your own sovereign intelligence system.

## Quick Rebrand

### 1. System Identity

Edit `backend/config.py`:

```python
SYSTEM_CONFIG = {
    "name": "YOUR_SYSTEM_NAME",        # e.g., "ATLAS", "NEXUS", "CORTEX"
    "tagline": "Your tagline here",
    "version": "1.0.0",
    "owner": "Your Organization",
    "owner_id": "TSID-0001",           # Your sovereign ID
}
```

### 2. Visual Identity

Edit `frontend/src/index.css` CSS variables:

```css
:root {
    --primary: 16 100% 50%;        /* Your brand color in HSL */
    --background: 0 0% 2%;         /* Dark background */
    /* ... */
}
```

Or update via the **Brand Profiles** admin UI after login.

### 3. Logo

Replace `frontend/public/logo.png` with your logo.

Update `frontend/src/App.js` sidebar:
```jsx
<span className="font-mono text-xl font-bold text-primary">
    YOUR_NAME
</span>
```

---

## Content Customization

### Seed Your Own Data

Edit `backend/seed.py` to define your own:

#### Documents
```python
DOCUMENTS = [
    {
        "filename": "architecture.pdf",
        "title": "System Architecture",
        "category": "Core",
        "description": "Your architecture overview"
    },
    # Add more...
]
```

#### Glossary Terms
```python
GLOSSARY = [
    {
        "term": "YOUR_TERM",
        "definition": "Definition here",
        "category": "Core Concepts"
    },
    # Add more...
]
```

#### Operators (Pig Pen)
```python
PIGPEN_OPERATORS = [
    {
        "tai_d": "TAI-D-001",
        "name": "Core Resolver",
        "capabilities": "Intent inference, routing",
        "role": "Core Resolution",
        "authority": "Evaluate only",
        "status": "LOCKED",
        "category": "Core"
    },
    # Add your operators...
]
```

#### System Components
```python
COMPONENTS = [
    {
        "name": "LAYER_NAME",
        "description": "What this layer does",
        "status": "active",
        "layer": 0,  # 0 = top (sovereign)
        "key_functions": ["Function 1", "Function 2"]
    },
    # Define your authority hierarchy...
]
```

Then run:
```bash
# Clear existing data (optional)
mongosh --eval "use('your_db'); db.dropDatabase();"

# Seed fresh
python seed.py
```

---

## Schema Extensions

### Adding Custom Content Types

1. **Define Model** in `backend/server.py`:

```python
class CustomType(BaseModel):
    model_config = ConfigDict(extra="ignore")
    custom_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    # your fields...
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
```

2. **Add CRUD Endpoints**:

```python
@api_router.get("/custom")
async def get_custom_items():
    items = await db.custom_items.find({"is_active": True}, {"_id": 0}).to_list(1000)
    return {"items": items}

@api_router.post("/custom")
async def create_custom_item(item: CustomTypeCreate, request: Request):
    user = await require_editor(request)
    # ... create logic with versioning and audit
```

3. **Create Frontend Page** in `frontend/src/pages/CustomPage.js`

4. **Add to Navigation** in `frontend/src/App.js`:

```javascript
const getNavItems = (user) => {
    const items = [
        // existing items...
        { path: "/custom", icon: YourIcon, label: "CUSTOM" },
    ];
    return items;
};
```

---

## Authentication Options

### Option 1: Emergent Google OAuth (Default)

Get your key at [emergentagent.com](https://emergentagent.com).

### Option 2: Your Own OAuth Provider

Replace the auth flow in `backend/server.py`:

```python
@api_router.post("/auth/session")
async def create_session(request: Request, response: Response):
    body = await request.json()
    # Your OAuth validation logic
    # ...
```

Update `frontend/src/pages/Login.js`:

```javascript
const handleLogin = () => {
    const redirectUrl = window.location.origin + '/';
    window.location.href = `YOUR_OAUTH_URL?redirect=${encodeURIComponent(redirectUrl)}`;
};
```

### Option 3: Simple JWT Auth

See `docs/JWT_AUTH.md` for a self-contained JWT implementation.

---

## AI Assistant Customization

### Change the System Prompt

Edit `SYSTEM_MESSAGE` in `backend/server.py`:

```python
SYSTEM_MESSAGE = """You are [YOUR_AI_NAME], the intelligence assistant for [YOUR_SYSTEM].

You are knowledgeable about:
- [Your domain]
- [Your concepts]
- [Your architecture]

Respond in a [your tone] manner."""
```

### Change the AI Model

```python
chat = LlmChat(
    api_key=api_key,
    session_id=session_id,
    system_message=SYSTEM_MESSAGE
).with_model("openai", "gpt-4o")  # or "anthropic", "claude-sonnet-4-5-20250929"
```

---

## Deployment

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| MONGO_URL | MongoDB connection string | Yes |
| DB_NAME | Database name | Yes |
| CORS_ORIGINS | Allowed origins (comma-separated) | Yes |
| EMERGENT_LLM_KEY | AI key for chat | For AI features |
| REACT_APP_BACKEND_URL | Backend URL for frontend | Yes |

### Production Checklist

- [ ] Set secure `CORS_ORIGINS` (not `*`)
- [ ] Use MongoDB Atlas or secured instance
- [ ] Enable HTTPS
- [ ] Set strong session secrets
- [ ] Configure rate limiting
- [ ] Set up monitoring/logging

---

## Examples

### Example: Legal Document System

```python
# config.py
SYSTEM_CONFIG = {
    "name": "LEXIS",
    "tagline": "Sovereign Legal Intelligence",
    "owner": "Law Firm LLC",
}

# seed.py - Custom operators
PIGPEN_OPERATORS = [
    {"tai_d": "TAI-D-001", "name": "Contract Analyzer", ...},
    {"tai_d": "TAI-D-002", "name": "Compliance Checker", ...},
    {"tai_d": "TAI-D-003", "name": "Risk Assessor", ...},
]
```

### Example: Creative Studio System

```python
# config.py
SYSTEM_CONFIG = {
    "name": "MUSE",
    "tagline": "Creative Intelligence Engine",
    "owner": "Studio Name",
}

# seed.py - Custom operators
PIGPEN_OPERATORS = [
    {"tai_d": "TAI-D-001", "name": "Brand Guardian", ...},
    {"tai_d": "TAI-D-002", "name": "Style Enforcer", ...},
    {"tai_d": "TAI-D-003", "name": "Narrative Director", ...},
]
```

---

Need help? Open an issue or discussion on GitHub.
