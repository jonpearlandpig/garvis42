# API Reference

Base URL: `http://localhost:8001/api` (development)

## Authentication

### Exchange OAuth Session
```http
POST /api/auth/session
Content-Type: application/json

{"session_id": "from_oauth_redirect"}
```

Response:
```json
{
  "user_id": "user_abc123",
  "email": "user@example.com",
  "name": "User Name",
  "picture": "https://...",
  "role": "admin"
}
```
Sets `session_token` cookie.

### Get Current User
```http
GET /api/auth/me
Cookie: session_token=...
```

### Logout
```http
POST /api/auth/logout
Cookie: session_token=...
```

---

## Documents

### List Documents
```http
GET /api/documents?category=Core&search=architecture
```

### Get Document
```http
GET /api/documents/{doc_id}
```

### Create Document (Editor+)
```http
POST /api/documents
Cookie: session_token=...
Content-Type: application/json

{
  "filename": "guide.pdf",
  "title": "User Guide",
  "category": "Guides",
  "description": "How to use the system",
  "content": "..."
}
```

### Update Document (Editor+)
```http
PUT /api/documents/{doc_id}
Cookie: session_token=...
Content-Type: application/json

{
  "title": "Updated Title",
  "description": "New description"
}
```

### Delete Document (Editor+)
```http
DELETE /api/documents/{doc_id}
Cookie: session_token=...
```

### Get Categories
```http
GET /api/documents/categories/list
```

---

## Glossary

### List Terms
```http
GET /api/glossary?category=Core&search=authority
```

### Create Term (Editor+)
```http
POST /api/glossary
Cookie: session_token=...
Content-Type: application/json

{
  "term": "NEW_TERM",
  "definition": "What it means",
  "category": "Core Concepts"
}
```

### Update Term (Editor+)
```http
PUT /api/glossary/{term_id}
```

### Delete Term (Editor+)
```http
DELETE /api/glossary/{term_id}
```

---

## Pig Pen Operators

### List Operators
```http
GET /api/pigpen?category=Business
```

### Get Operator
```http
GET /api/pigpen/{operator_id}
```

### Create Operator (Editor+)
```http
POST /api/pigpen
Cookie: session_token=...
Content-Type: application/json

{
  "tai_d": "TAI-D-100",
  "name": "Custom Analyzer",
  "capabilities": "Analysis and reporting",
  "role": "Analysis",
  "authority": "Recommend only",
  "status": "ACTIVE",
  "category": "Custom"
}
```

### Update Operator (Editor+)
```http
PUT /api/pigpen/{operator_id}
```

### Delete Operator (Editor+)
```http
DELETE /api/pigpen/{operator_id}
```

---

## Brand Profiles

### List Brands
```http
GET /api/brands
```

### Create Brand (Editor+)
```http
POST /api/brands
Cookie: session_token=...
Content-Type: application/json

{
  "name": "Dark Theme",
  "description": "High contrast dark mode",
  "primary_color": "#FF4500",
  "secondary_color": "#1A1A1A",
  "font_heading": "JetBrains Mono",
  "font_body": "Manrope",
  "style_guidelines": "Sharp edges, no rounded corners"
}
```

### Update Brand (Editor+)
```http
PUT /api/brands/{brand_id}
```

### Delete Brand (Editor+)
```http
DELETE /api/brands/{brand_id}
```

---

## Architecture Components

### List Components
```http
GET /api/architecture/components
```

### Update Component (Editor+)
```http
PUT /api/architecture/components/{component_id}
Cookie: session_token=...
Content-Type: application/json

{
  "description": "Updated description",
  "status": "active",
  "key_functions": ["Function 1", "Function 2"]
}
```

---

## Audit Log

### Get Audit Log (Auth Required)
```http
GET /api/audit-log?content_type=pigpen&limit=50
Cookie: session_token=...
```

Response:
```json
{
  "entries": [
    {
      "log_id": "uuid",
      "user_id": "user_abc",
      "user_name": "John Doe",
      "action": "update",
      "content_type": "pigpen",
      "content_id": "op_xyz",
      "content_title": "Risk Analyzer",
      "details": {"changes": ["capabilities"]},
      "timestamp": "2026-02-13T22:00:00Z"
    }
  ]
}
```

---

## Version History

### Get Versions
```http
GET /api/versions/{content_type}/{content_id}
Cookie: session_token=...
```

Content types: `document`, `glossary`, `component`, `pigpen`, `brand`

### Rollback to Version (Editor+)
```http
POST /api/versions/{content_type}/{content_id}/rollback/{version_id}
Cookie: session_token=...
```

---

## Admin (Admin Only)

### List Users
```http
GET /api/admin/users
Cookie: session_token=...
```

### Update User Role
```http
PUT /api/admin/users/{user_id}/role
Cookie: session_token=...
Content-Type: application/json

{"role": "editor"}
```

Valid roles: `viewer`, `editor`, `admin`

---

## Chat (AI Assistant)

### Send Message
```http
POST /api/chat
Content-Type: application/json

{
  "message": "What is GARVIS?",
  "session_id": "optional_session_id"
}
```

Response:
```json
{
  "response": "GARVIS is the sovereign intelligence...",
  "session_id": "chat_session_123"
}
```

### Get Chat History
```http
GET /api/chat/history/{session_id}
```

### Clear Session
```http
DELETE /api/chat/session/{session_id}
```

---

## Dashboard

### Get Stats
```http
GET /api/dashboard/stats
```

Response:
```json
{
  "total_documents": 18,
  "total_glossary_terms": 30,
  "total_components": 8,
  "total_pigpen_operators": 18,
  "total_brand_profiles": 1,
  "system_status": "OPERATIONAL",
  "authority_chain": "INTACT"
}
```

---

## Health Check

```http
GET /api/health
```

Response:
```json
{
  "status": "healthy",
  "timestamp": "2026-02-13T22:00:00Z"
}
```
