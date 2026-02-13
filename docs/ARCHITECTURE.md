# System Architecture

## Overview

GARVIS Full Stack implements a sovereign intelligence architecture with clear authority hierarchy, content governance, and audit capabilities.

## Authority Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    SOVEREIGN AUTHORITY                       │
│              (Human) Constitutional Control                  │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                      TELAUTHORIUM                            │
│           Authorship • Provenance • Rights Registry          │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                         GARVIS                               │
│        Sovereign Intelligence • Truth Enforcement            │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                     FLIGHTPATH COS                           │
│     Phase Discipline • SPARK→BUILD→LAUNCH→EXPAND→SUNSET     │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                          MOSE                                │
│           Operator Routing • Escalation Logic                │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                        PIG PEN                               │
│       Non-Human Operators (TAI-D) • Analysis & Flags         │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                          TELA                                │
│              Execution Layer • Adapter Tooling               │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                   AUDIT & EVENT LEDGER                       │
│              Immutable Record • All Actions Logged           │
└─────────────────────────────────────────────────────────────┘
```

## Core Principle

> Authority flows top-down. No component can override one above it.
> Execution only happens at TELA. All actions logged to Audit Ledger.

---

## Technical Architecture

### Stack

```
┌─────────────────────────────────────────────────────────────┐
│                        FRONTEND                              │
│                  React 19 + Tailwind CSS                     │
│                    Shadcn UI Components                      │
└─────────────────────────┬───────────────────────────────────┘
                          │ HTTP/REST
┌─────────────────────────▼───────────────────────────────────┐
│                        BACKEND                               │
│                    FastAPI (Python)                          │
│              Auth • CRUD • Versioning • AI                   │
└─────────────────────────┬───────────────────────────────────┘
                          │ Motor (Async)
┌─────────────────────────▼───────────────────────────────────┐
│                        DATABASE                              │
│                        MongoDB                               │
│     users • content • versions • audit_log • sessions        │
└─────────────────────────────────────────────────────────────┘
```

### Data Model

```
┌──────────────────┐     ┌──────────────────┐
│      users       │     │   user_sessions  │
├──────────────────┤     ├──────────────────┤
│ user_id (UUID)   │────▶│ user_id          │
│ email            │     │ session_token    │
│ name             │     │ expires_at       │
│ role             │     └──────────────────┘
│ created_at       │
└──────────────────┘
         │
         │ changed_by
         ▼
┌──────────────────┐     ┌──────────────────┐
│   audit_log      │     │ content_versions │
├──────────────────┤     ├──────────────────┤
│ log_id           │     │ version_id       │
│ user_id          │     │ content_id       │
│ action           │     │ content_type     │
│ content_type     │     │ data (snapshot)  │
│ content_id       │     │ changed_by       │
│ timestamp        │     │ change_type      │
└──────────────────┘     │ timestamp        │
                         └──────────────────┘

┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│    documents     │  │  glossary_terms  │  │    components    │
├──────────────────┤  ├──────────────────┤  ├──────────────────┤
│ doc_id           │  │ term_id          │  │ component_id     │
│ title            │  │ term             │  │ name             │
│ category         │  │ definition       │  │ description      │
│ content          │  │ category         │  │ layer            │
│ is_active        │  │ is_active        │  │ key_functions    │
└──────────────────┘  └──────────────────┘  └──────────────────┘

┌──────────────────┐  ┌──────────────────┐
│ pigpen_operators │  │  brand_profiles  │
├──────────────────┤  ├──────────────────┤
│ operator_id      │  │ brand_id         │
│ tai_d            │  │ name             │
│ name             │  │ primary_color    │
│ capabilities     │  │ secondary_color  │
│ role             │  │ font_heading     │
│ authority        │  │ font_body        │
│ status           │  │ style_guidelines │
│ category         │  └──────────────────┘
└──────────────────┘
```

---

## Request Flow

### Read Operation
```
Client → GET /api/documents → Backend → MongoDB → Response
```

### Write Operation (Authenticated)
```
Client → POST /api/documents
    │
    ▼
Backend validates session_token (cookie/header)
    │
    ▼
Check user role (editor/admin required)
    │
    ▼
Save current state to content_versions
    │
    ▼
Perform update in MongoDB
    │
    ▼
Log to audit_log
    │
    ▼
Response
```

### Rollback Operation
```
Client → POST /api/versions/{type}/{id}/rollback/{version_id}
    │
    ▼
Fetch target version snapshot
    │
    ▼
Save current state as new version ("before rollback")
    │
    ▼
Restore target version data
    │
    ▼
Save restored state as new version ("rollback")
    │
    ▼
Log rollback to audit_log
    │
    ▼
Response
```

---

## Security Model

### Authentication
- OAuth 2.0 via Emergent (Google)
- Session tokens stored in httpOnly cookies
- 7-day session expiry

### Authorization
| Role | Read | Create | Update | Delete | Admin |
|------|------|--------|--------|--------|-------|
| Viewer | ✓ | ✗ | ✗ | ✗ | ✗ |
| Editor | ✓ | ✓ | ✓ | ✓ | ✗ |
| Admin | ✓ | ✓ | ✓ | ✓ | ✓ |

### First User = Admin
The first user to authenticate automatically receives admin role.

---

## Audit Trail

Every mutation is logged:

```json
{
  "log_id": "uuid",
  "user_id": "user_abc123",
  "user_name": "John Doe",
  "user_email": "john@example.com",
  "action": "update",
  "content_type": "pigpen",
  "content_id": "operator_xyz",
  "content_title": "Risk Analyzer",
  "details": {"changes": ["capabilities", "status"]},
  "timestamp": "2026-02-13T22:00:00Z"
}
```

---

## Version Control

Every content change creates a snapshot:

```json
{
  "version_id": "uuid",
  "content_id": "operator_xyz",
  "content_type": "pigpen",
  "data": { /* full document snapshot */ },
  "changed_by": "user_abc123",
  "changed_by_name": "John Doe",
  "change_type": "update",
  "change_summary": "Updated capabilities",
  "timestamp": "2026-02-13T22:00:00Z"
}
```

Rollback restores any previous snapshot while preserving history.
