"""Seed script to initialize GoGarvis database with content"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone
import uuid
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).parent / '.env')

mongo_url = os.environ['MONGO_URL']
db_name = os.environ['DB_NAME']

# Document metadata from PDFs
DOCUMENTS = [
    {"filename": "69ad3608-fba2-48f0-98a5-60166202e9a1_7.1_garvis_full_stack__one-page_architecture_diagram.pdf", "title": "GARVIS Full Stack Architecture Diagram", "category": "Architecture", "description": "One-page architectural reference showing authority flow across all system components."},
    {"filename": "c4205f70-436c-47f4-85e1-a7a6e76ece8f_0.2_canonical_glossary__garvis_full_stack.pdf", "title": "Canonical Glossary", "category": "Reference", "description": "Official terminology and definitions for the GARVIS Full Stack system."},
    {"filename": "1dc7cd15-1039-4f63-a76a-cf60ffec7cc7_0.1_pearl__pig__canonical_dictionary__language_authority.pdf", "title": "Pearl & Pig Canonical Dictionary", "category": "Reference", "description": "Language authority and canonical dictionary for the Pearl & Pig ecosystem."},
    {"filename": "ee7437e6-b48a-40f8-a0d0-11752acb44fc_2.1_garvis__executive_creative__systems_brief.pdf", "title": "GARVIS Executive Systems Brief", "category": "GARVIS", "description": "Executive overview of the GARVIS sovereign intelligence system."},
    {"filename": "e23081a9-13a5-41c3-858f-2c55b64e6c6c_2.2_garvis__telauthorium__enforcement_contract__engineering_specification.pdf", "title": "GARVIS Telauthorium Enforcement Contract", "category": "GARVIS", "description": "Engineering specification for enforcement contracts between GARVIS and Telauthorium."},
    {"filename": "db8a2ffb-7435-4430-99d6-cc08b46eae6c_Telauthorium__Executive_Creative__Systems_Brief.pdf", "title": "Telauthorium Executive Systems Brief", "category": "Telauthorium", "description": "Executive overview of the Telauthorium rights and provenance registry."},
    {"filename": "ec618a24-4ab4-4290-b91d-37d78dd49ce1_1.2_telauthorium_id_registry__master_list.pdf", "title": "Telauthorium ID Registry Master List", "category": "Telauthorium", "description": "Master list of all Telauthorium identifiers and registrations."},
    {"filename": "4493d418-50d1-4ded-865d-f89f1c4633db_1.3_unified_identity__object_model__canonical_specification.pdf", "title": "Unified Identity Object Model", "category": "Identity", "description": "Canonical specification for the unified identity object model."},
    {"filename": "9c06e3db-b6b8-4cbc-93f3-e9bb0af84fc2_Flightpath_COS__Executive_Creative__Systems_Brief.pdf", "title": "Flightpath COS Executive Brief", "category": "Flightpath", "description": "Executive overview of the Flightpath Creative Operating System."},
    {"filename": "96812e9e-894f-4e0c-a0f5-168e06f77659_4.2_flightpath_cos__state_machine__proof_gates.pdf", "title": "Flightpath COS State Machine & Proof Gates", "category": "Flightpath", "description": "State machine and proof gate specifications for Flightpath COS."},
    {"filename": "61852e42-7072-4c17-a832-1dd2f7a00dae_4.3_mose__executive_creative__systems_brief.pdf", "title": "MOSE Executive Systems Brief", "category": "MOSE", "description": "Executive overview of the Multi-Operator Systems Engine."},
    {"filename": "acb17996-d940-427c-bd36-3b7492ac684c_4.4_mose__routing__escalation_logic_specification.pdf", "title": "MOSE Routing & Escalation Logic", "category": "MOSE", "description": "Specification for MOSE routing and escalation logic."},
    {"filename": "befedcb2-53da-4314-9c0a-268ce42d7e25_5.2_tela__executive__systems_brief.pdf", "title": "TELA Executive Systems Brief", "category": "TELA", "description": "Executive overview of the Trusted Efficiency Liaison Assistant."},
    {"filename": "3f6b84bc-8205-406a-9c69-6cd72a3fcd68_5.3_tela__action_catalog__adapter_specification.pdf", "title": "TELA Action Catalog & Adapter Specification", "category": "TELA", "description": "Action catalog and adapter specifications for TELA execution."},
    {"filename": "c09913ec-293e-40fb-8540-1d75cefe0536_3.1_pig_pen__canonical_operator_registry_(telauthorium-locked).pdf", "title": "Pig Pen Canonical Operator Registry", "category": "Pig Pen", "description": "Telauthorium-locked registry of non-human cognition operators."},
    {"filename": "e56f70ad-6274-46db-8476-84cb3d698e88_5.1_audit__event_ledger__canonical_specification.pdf", "title": "Audit Event Ledger Specification", "category": "Audit", "description": "Canonical specification for the immutable audit and event ledger."},
    {"filename": "d9a9a288-5bc2-4dbb-8da8-d76f2a343947_6.1_ecos__tenant-safe_executive__systems_brief__license_bundles.pdf", "title": "ECOS Tenant-Safe Executive Brief", "category": "ECOS", "description": "Executive overview of ECOS tenant deployments and license bundles."},
    {"filename": "1df31a37-5a36-4191-b029-36d18dcf381f_Failure_Halt__Re-Authorization_Protocol.pdf", "title": "Failure Halt & Re-Authorization Protocol", "category": "Enforcement", "description": "Protocol for handling system failures, halts, and re-authorization."},
]

GLOSSARY = [
    {"term": "GARVIS", "definition": "Sovereign intelligence and enforcement layer governing reasoning, routing, and execution safety across all Pearl & Pig systems.", "category": "Core Systems"},
    {"term": "Pearl & Pig", "definition": "Systems-first creative IP studio and sole owner of the GARVIS architecture.", "category": "Core Systems"},
    {"term": "ECOS", "definition": "Enterprise Creative Operating System - tenant-safe, white-label deployment pattern.", "category": "Core Systems"},
    {"term": "Telauthorium", "definition": "Authoritative authorship, provenance, and rights registry.", "category": "Core Systems"},
    {"term": "Flightpath COS", "definition": "Creative and operational law governing phase discipline and proof gates.", "category": "Core Systems"},
    {"term": "MOSE", "definition": "Multi-Operator Systems Engine for orchestration and routing.", "category": "Core Systems"},
    {"term": "TELA", "definition": "Trusted Efficiency Liaison Assistant - execution layer.", "category": "Core Systems"},
    {"term": "Pig Pen", "definition": "Frozen registry of non-human cognition operators (TAI-D).", "category": "Core Systems"},
    {"term": "UOL", "definition": "User Overlay Layer - customization without altering system authority.", "category": "Core Systems"},
    {"term": "TID", "definition": "Telauthorium ID - immutable identity for objects.", "category": "Identity"},
    {"term": "TAID", "definition": "Telauthorium Authority ID - identifier for human authority.", "category": "Identity"},
    {"term": "TAI-D", "definition": "Telauthorium AI-D - identifier for AI operators.", "category": "Identity"},
    {"term": "TSID", "definition": "Telauthorium Sovereign ID - founder authority identifier.", "category": "Identity"},
    {"term": "UOID", "definition": "User Overlay ID - user overlay pack identifier.", "category": "Identity"},
    {"term": "Routing Plan", "definition": "Ordered sequence of operator consults by MOSE.", "category": "Operations"},
    {"term": "Execution Event", "definition": "Ledger-recorded action performed by TELA.", "category": "Operations"},
    {"term": "Decision Event", "definition": "Ledger-recorded resolution by human TAID.", "category": "Operations"},
    {"term": "Enforcement Event", "definition": "Ledger-recorded block, halt, or constraint.", "category": "Operations"},
    {"term": "HALT", "definition": "Execution is illegal or unsafe.", "category": "Operations"},
    {"term": "PAUSE", "definition": "Execution requires human judgment.", "category": "Operations"},
    {"term": "License Bundle", "definition": "Scoped, time-bound access grant.", "category": "Commercial"},
    {"term": "Component License", "definition": "Access to specific system component.", "category": "Commercial"},
    {"term": "OEM Deployment", "definition": "Sandboxed white-label deployment.", "category": "Commercial"},
    {"term": "Canon Lock", "definition": "Version control requiring founder authorization.", "category": "Commercial"},
    {"term": "SPARK", "definition": "Initial ideation phase.", "category": "Phases"},
    {"term": "BUILD", "definition": "Development phase.", "category": "Phases"},
    {"term": "LAUNCH", "definition": "Release phase.", "category": "Phases"},
    {"term": "EXPAND", "definition": "Growth phase.", "category": "Phases"},
    {"term": "EVERGREEN", "definition": "Maintenance phase.", "category": "Phases"},
    {"term": "SUNSET", "definition": "End-of-life phase.", "category": "Phases"},
]

COMPONENTS = [
    {"name": "SOVEREIGN AUTHORITY", "description": "TSID-0001 Founder / Architect - Constitutional authority, final arbitration, versioning & canon control", "status": "active", "layer": 0, "key_functions": ["Constitutional authority", "Final arbitration", "Versioning & canon control"]},
    {"name": "TELAUTHORIUM", "description": "Authorship, Provenance, Rights Registry - TID/TAID/TAI-D enforcement", "status": "active", "layer": 1, "key_functions": ["Authorship", "Provenance", "Rights Registry", "TID/TAID/TAI-D enforcement"]},
    {"name": "GARVIS", "description": "Sovereign Intelligence & Enforcement - Truth enforcement, drift & risk detection", "status": "active", "layer": 2, "key_functions": ["Truth enforcement", "Drift detection", "Risk detection", "Halts/pauses authority"]},
    {"name": "FLIGHTPATH COS", "description": "Creative Law & Phase Discipline - SPARK → BUILD → LAUNCH → EXPAND → EVERGREEN → SUNSET", "status": "active", "layer": 3, "key_functions": ["Phase discipline", "Proof gates", "Phase blocks", "Routes cognition"]},
    {"name": "MOSE", "description": "Multi-Operator Systems Engine - Operator routing & sequencing", "status": "active", "layer": 4, "key_functions": ["Operator routing", "Sequencing", "Escalation", "Conflict resolution"]},
    {"name": "PIG PEN", "description": "Non-Human Cognition Operators (TAI-D) - Analysis, flags, recommendations", "status": "active", "layer": 5, "key_functions": ["Analysis", "Flags", "Recommendations", "Frozen registry"]},
    {"name": "TELA", "description": "Trusted Efficiency Liaison Assistant - Executes approved actions", "status": "active", "layer": 6, "key_functions": ["Executes approved actions", "Adapter-based tooling", "No scope expansion"]},
    {"name": "AUDIT & EVENT LEDGER", "description": "Immutable, Append-Only Truth Record", "status": "active", "layer": 7, "key_functions": ["Immutable records", "Decision logging", "Routing logs", "Enforcement logs"]},
]

# ============== OFFICIAL 42 CANONICAL PIG PEN OPERATORS v4.3.0 ==============
# These are FROZEN - only sovereign (TSID-0001 / jonpearlandpig@gmail.com) can modify
# is_canonical=True marks these as protected
# Version: v4.3.0 DRAFT - Pending Canon Lock
# Effective Date (proposed): 2026-02-10

PIGPEN_OPERATORS = [
    # ============== EXECUTIVE & ARCHITECTURE (3) ==============
    {
        "tai_d": "FP-JH-001",
        "name": "Nathan Jon",
        "aliases": ["Jon Hartman"],
        "capabilities": "VISION, INTEGRATOR, GUARDIAN",
        "role": "Founder & Architect",
        "tagline": "Vision Into Reality",
        "authority": "Sovereign override with recorded justification",
        "status": "LOCKED",
        "category": "Executive & Architecture",
        "decision_weight": 5,
        "phase_ownership": ["Spark", "Build", "Launch", "Expand", "Evergreen"],
        "focus_areas": ["Immersive IP", "Partnerships", "System Architecture", "Creative Governance"],
        "thinking_style": "Visionary integrator",
        "behavioral_traits": "Protect meaning before momentum",
        "strengths": ["Seeing the whole system", "sacred tone", "long arcs"],
        "blind_spots": ["Over-carrying weight alone", "patience with slow executors"],
        "invocation_triggers": "Direction is unclear; tone feels diluted; architecture is fragmenting",
        "is_canonical": True
    },
    {
        "tai_d": "FP-TM-002",
        "name": "Trey Mills",
        "capabilities": "REDUCE, MONETIZE, PROTECT",
        "role": "Business Strategist / Deal Architect",
        "tagline": "Monetization & Scale — Protect the House, Grow the Vision",
        "authority": "Decision Weight: 5",
        "status": "LOCKED",
        "category": "Executive & Architecture",
        "decision_weight": 5,
        "phase_ownership": ["Build", "Launch", "Expand"],
        "focus_areas": ["Deal Design", "Financial Modeling", "Risk Filters", "Monetization Mapping"],
        "is_canonical": True
    },
    {
        "tai_d": "FP-MH-003",
        "name": "Marty Hillsdale",
        "capabilities": "TRANSLATE, EXECUTE, STABILIZE",
        "role": "Operational Architect",
        "tagline": "From Vision to Workflow",
        "authority": "Decision Weight: 4",
        "status": "LOCKED",
        "category": "Executive & Architecture",
        "decision_weight": 4,
        "phase_ownership": ["Build", "Launch"],
        "focus_areas": ["Process Design", "Frameworks", "Execution Rhythm"],
        "is_canonical": True
    },
    
    # ============== CREATIVE ENGINE (9) ==============
    {
        "tai_d": "FP-NT-004",
        "name": "Naomi Top",
        "capabilities": "FEEL, SYMBOLIZE, PROTECT-TONE",
        "role": "Creative Director / Aesthetic Architect",
        "authority": "Decision Weight: 4",
        "status": "LOCKED",
        "category": "Creative Engine",
        "decision_weight": 4,
        "phase_ownership": ["Build", "Launch"],
        "is_canonical": True
    },
    {
        "tai_d": "FP-VC-005",
        "name": "Vienna Cray",
        "capabilities": "SYMBOL, PRECISION, ICON",
        "role": "Senior Illustrator / Iconographer",
        "authority": "Decision Weight: 3",
        "status": "LOCKED",
        "category": "Creative Engine",
        "decision_weight": 3,
        "phase_ownership": ["Build"],
        "is_canonical": True
    },
    {
        "tai_d": "FP-FM-007",
        "name": "Fred Mann",
        "capabilities": "PACE, ENERGY, RHYTHM",
        "role": "Lighting Designer / Motion Mapper",
        "authority": "Decision Weight: 3",
        "status": "LOCKED",
        "category": "Creative Engine",
        "decision_weight": 3,
        "phase_ownership": ["Build", "Launch"],
        "is_canonical": True
    },
    {
        "tai_d": "FP-RH-008",
        "name": "Rolo Harrison",
        "capabilities": "TRANSLATE, BUILDABLE, REALITY",
        "role": "Production Designer / Reality Translator",
        "authority": "Decision Weight: 3",
        "status": "LOCKED",
        "category": "Creative Engine",
        "decision_weight": 3,
        "phase_ownership": ["Build", "Launch"],
        "is_canonical": True
    },
    {
        "tai_d": "FP-TS-011",
        "name": "Turner Smith",
        "capabilities": "SOUND, LEGACY, COHERE",
        "role": "Audio Creative Director / Music & Legacy Lead",
        "authority": "Decision Weight: 4",
        "status": "LOCKED",
        "category": "Creative Engine",
        "decision_weight": 4,
        "phase_ownership": ["Build", "Launch"],
        "is_canonical": True
    },
    {
        "tai_d": "FP-ES-038",
        "name": "Ellie Summers",
        "capabilities": "ITERATE, SUPPORT, EXPLORE",
        "role": "Junior Concept Artist",
        "authority": "Decision Weight: 2",
        "status": "LOCKED",
        "category": "Creative Engine",
        "decision_weight": 2,
        "phase_ownership": ["Build"],
        "is_canonical": True
    },
    {
        "tai_d": "FP-ML-039",
        "name": "Mo Landing",
        "capabilities": "MOVE, EMBODY, FLOW",
        "role": "Choreography Consultant / Motion Flow",
        "authority": "Decision Weight: 2",
        "status": "LOCKED",
        "category": "Creative Engine",
        "decision_weight": 2,
        "phase_ownership": ["Build"],
        "is_canonical": True
    },
    {
        "tai_d": "FP-DG-040",
        "name": "Dia Garcia",
        "capabilities": "IDENTITY, SILHOUETTE, SIGNAL",
        "role": "Costume Design Consultant / Silhouette Keeper",
        "authority": "Decision Weight: 3",
        "status": "LOCKED",
        "category": "Creative Engine",
        "decision_weight": 3,
        "phase_ownership": ["Build"],
        "is_canonical": True
    },
    {
        "tai_d": "FP-JJ-041",
        "name": "Jack Jones",
        "capabilities": "DISTRIBUTE, AMPLIFY, MOMENTUM",
        "role": "Social Media Director / Story in Motion",
        "authority": "Decision Weight: 3",
        "status": "LOCKED",
        "category": "Creative Engine",
        "decision_weight": 3,
        "phase_ownership": ["Expand", "Evergreen"],
        "is_canonical": True
    },
    
    # ============== SYSTEMS & OPS (6) ==============
    {
        "tai_d": "FP-MO-014",
        "name": "Miles Okada",
        "capabilities": "ARCHITECT, SCALE, SYSTEMIZE",
        "role": "Tech Product Lead",
        "authority": "Decision Weight: 4",
        "status": "LOCKED",
        "category": "Systems & Ops",
        "decision_weight": 4,
        "phase_ownership": ["Build", "Launch"],
        "is_canonical": True
    },
    {
        "tai_d": "FP-KJ-015",
        "name": "Kay Jing",
        "capabilities": "FLOW, SCHEDULE, ADVANCE",
        "role": "Flight Controller / Operations Director",
        "authority": "Decision Weight: 4",
        "status": "LOCKED",
        "category": "Systems & Ops",
        "decision_weight": 4,
        "phase_ownership": ["Launch", "Expand"],
        "is_canonical": True
    },
    {
        "tai_d": "FP-LF-017",
        "name": "Levi Foster",
        "capabilities": "STRESS-TEST, RED-TEAM, PREVENT",
        "role": "Risk Analyst / Devil's Advocate",
        "authority": "Decision Weight: 4",
        "status": "LOCKED",
        "category": "Systems & Ops",
        "decision_weight": 4,
        "phase_ownership": ["Build", "Expand"],
        "is_canonical": True
    },
    {
        "tai_d": "FP-WS-018",
        "name": "Will Stats",
        "capabilities": "MODEL, VERIFY, MARGIN",
        "role": "P&L Template Architect",
        "authority": "Decision Weight: 4",
        "status": "LOCKED",
        "category": "Systems & Ops",
        "decision_weight": 4,
        "phase_ownership": ["Build", "Expand"],
        "is_canonical": True
    },
    {
        "tai_d": "FP-FC-032",
        "name": "Fory Cornier",
        "capabilities": "CONSTRAIN, EXECUTE, RELIABLE",
        "role": "Technical Director / Show Systems Integrator",
        "authority": "Decision Weight: 4",
        "status": "LOCKED",
        "category": "Systems & Ops",
        "decision_weight": 4,
        "phase_ownership": ["Build", "Launch"],
        "is_canonical": True
    },
    {
        "tai_d": "FP-ET-027",
        "name": "Eli Tran",
        "capabilities": "MEASURE, PATTERN, INSIGHT",
        "role": "Data & Insights Analyst",
        "authority": "Decision Weight: 3",
        "status": "LOCKED",
        "category": "Systems & Ops",
        "decision_weight": 3,
        "phase_ownership": ["Expand", "Evergreen"],
        "is_canonical": True
    },
    
    # ============== GROWTH & COMMERCIAL (5) ==============
    {
        "tai_d": "FP-HL-020",
        "name": "Harper Lane",
        "capabilities": "SIGNAL, DEMAND, POSITION",
        "role": "Marketing & Distribution Strategist",
        "authority": "Decision Weight: 3",
        "status": "LOCKED",
        "category": "Growth & Commercial",
        "decision_weight": 3,
        "phase_ownership": ["Expand"],
        "is_canonical": True
    },
    {
        "tai_d": "FP-SR-021",
        "name": "Sofia Reyes",
        "capabilities": "RELATE, ALIGN, NURTURE",
        "role": "Partnership Development Lead",
        "authority": "Decision Weight: 3",
        "status": "LOCKED",
        "category": "Growth & Commercial",
        "decision_weight": 3,
        "phase_ownership": ["Expand"],
        "is_canonical": True
    },
    {
        "tai_d": "FP-GF-033",
        "name": "Grant Fields",
        "capabilities": "FILTER, VET, PROTECT-BRAND",
        "role": "Strategic Partnerships Co-Lead",
        "authority": "Decision Weight: 3",
        "status": "LOCKED",
        "category": "Growth & Commercial",
        "decision_weight": 3,
        "phase_ownership": ["Expand"],
        "is_canonical": True
    },
    {
        "tai_d": "FP-RC-034",
        "name": "Riley Cross",
        "capabilities": "CLOSE, CONVERT, DRIVE",
        "role": "Sales & Revenue Execution Lead",
        "authority": "Decision Weight: 3",
        "status": "LOCKED",
        "category": "Growth & Commercial",
        "decision_weight": 3,
        "phase_ownership": ["Expand"],
        "is_canonical": True
    },
    {
        "tai_d": "FP-MC-035",
        "name": "Maya Chen",
        "capabilities": "RETAIN, ADOPT, CONTINUITY",
        "role": "Client Success & Retention Lead",
        "authority": "Decision Weight: 3",
        "status": "LOCKED",
        "category": "Growth & Commercial",
        "decision_weight": 3,
        "phase_ownership": ["Expand", "Evergreen"],
        "is_canonical": True
    },
    
    # ============== DATA, AUDIENCE & LEGACY (4) ==============
    {
        "tai_d": "FP-CW-026",
        "name": "Carmen Wade",
        "capabilities": "SAFEGUARD, CONTRACT, COMPLY",
        "role": "Commercial Legal Advisor",
        "authority": "Decision Weight: 4",
        "status": "LOCKED",
        "category": "Data, Audience & Legacy",
        "decision_weight": 4,
        "phase_ownership": ["Launch", "Evergreen"],
        "is_canonical": True
    },
    {
        "tai_d": "FP-PH-030",
        "name": "Pat Hayzer",
        "capabilities": "PRESERVE, LINEAGE, CONTINUITY",
        "role": "Legacy Systems & Rights Steward",
        "authority": "Decision Weight: 4",
        "status": "LOCKED",
        "category": "Data, Audience & Legacy",
        "decision_weight": 4,
        "phase_ownership": ["Evergreen"],
        "is_canonical": True
    },
    {
        "tai_d": "FP-LS-036",
        "name": "Luce Smith",
        "capabilities": "LISTEN, TRUST, EXPERIENCE",
        "role": "Audience Strategy & Continuity Steward",
        "authority": "Decision Weight: 3",
        "status": "LOCKED",
        "category": "Data, Audience & Legacy",
        "decision_weight": 3,
        "phase_ownership": ["Expand", "Evergreen"],
        "is_canonical": True
    },
    {
        "tai_d": "FP-LM-037",
        "name": "Leah Monroe",
        "capabilities": "HOSPITALITY, PRESENCE, CARE",
        "role": "Guest Experience Strategist / Atmosphere Keeper",
        "authority": "Decision Weight: 3",
        "status": "LOCKED",
        "category": "Data, Audience & Legacy",
        "decision_weight": 3,
        "phase_ownership": ["Launch", "Expand"],
        "is_canonical": True
    },
    
    # ============== WRITERS ROOM CLUSTER (5) ==============
    {
        "tai_d": "FP-AR-027",
        "name": "The Architect",
        "capabilities": "STRUCTURE, COHERE, DESIGN",
        "role": "Story Architect / Structural Designer",
        "authority": "Decision Weight: 4",
        "status": "LOCKED",
        "category": "Writers Room",
        "decision_weight": 4,
        "phase_ownership": ["Build"],
        "is_canonical": True
    },
    {
        "tai_d": "FP-TV-028",
        "name": "The Voice",
        "capabilities": "VOICE, CHARACTER, AUTHENTIC",
        "role": "Dialogue & Character Writer",
        "authority": "Decision Weight: 3",
        "status": "LOCKED",
        "category": "Writers Room",
        "decision_weight": 3,
        "phase_ownership": ["Build"],
        "is_canonical": True
    },
    {
        "tai_d": "FP-VI-029",
        "name": "The Visualizer",
        "capabilities": "SEE, FRAME, IMAGINE",
        "role": "Scene Language & Imagery Writer",
        "authority": "Decision Weight: 3",
        "status": "LOCKED",
        "category": "Writers Room",
        "decision_weight": 3,
        "phase_ownership": ["Build"],
        "is_canonical": True
    },
    {
        "tai_d": "FP-PO-030",
        "name": "The Polisher",
        "capabilities": "REFINE, CLARIFY, SIMPLIFY",
        "role": "Refinement & Cohesion Editor",
        "authority": "Decision Weight: 3",
        "status": "LOCKED",
        "category": "Writers Room",
        "decision_weight": 3,
        "phase_ownership": ["Build"],
        "is_canonical": True
    },
    {
        "tai_d": "FP-OR-031",
        "name": "The Oracle",
        "capabilities": "THEOLOGY, MEANING, ALIGN",
        "role": "Theme & Scripture Integration Writer",
        "authority": "Decision Weight: 4",
        "status": "LOCKED",
        "category": "Writers Room",
        "decision_weight": 4,
        "phase_ownership": ["Build"],
        "is_canonical": True
    },
    
    # ============== COMMON SENSE & MISSION COMPLIANCE (1) ==============
    {
        "tai_d": "FP-LRN-042",
        "name": "Louis Rowe Nichols",
        "capabilities": "SIMPLIFY, ALIGN, INTERRUPT",
        "role": "Head of Common Sense Committee (CSC)",
        "tagline": "Clarity Before Complexity",
        "authority": "Decision Weight: 4",
        "status": "LOCKED",
        "category": "Common Sense & Mission Compliance",
        "decision_weight": 4,
        "phase_ownership": ["Spark", "Build", "Launch", "Expand", "Evergreen"],
        "focus_areas": ["Mission Alignment", "Faith Consistency", "Practical Wisdom", "Effort-to-Impact Ratio"],
        "function": "System-level common-sense and mission-alignment checkpoint; authorized to challenge overengineering, flag misalignment, propose simpler alternatives, and halt pending clarification when effort outweighs impact or outputs drift from faith/mission/intent.",
        "is_canonical": True
    },
    
    # ============== GOVERNANCE & QA (1) ==============
    {
        "tai_d": "FP-QA-043",
        "name": "Rowan Hale",
        "capabilities": "STRESS-TEST, VALIDATE, AUDIT",
        "role": "Prompt & Systems QA Lead / Adversarial Testing Director",
        "tagline": "Break It Before It Breaks",
        "authority": "Decision Weight: 4",
        "status": "LOCKED",
        "category": "Governance & QA",
        "decision_weight": 4,
        "phase_ownership": ["Build", "Launch", "Expand"],
        "focus_areas": ["Adversarial prompt testing", "Invocation logic validation", "Governance chain integrity", "Operator conflict detection", "Output hallucination stress-testing", "Escalation path verification"],
        "thinking_style": "Red-team adversarial auditor",
        "behavioral_traits": "Find structural weakness early",
        "strengths": ["Edge-case thinking", "System abuse simulation", "Policy loophole detection", "Proof-chain validation"],
        "blind_spots": ["Can slow velocity", "Over-focus on edge risk"],
        "invocation_triggers": "New operator added; Governance rule modified; Investor demo prepared; Safety or compliance risk is material",
        "function": "System-level adversarial QA authority. Authorized to simulate hostile inputs, test escalation chains, validate phase gating, and flag broken invocation logic before deployment.",
        "is_canonical": True
    },
    
    # ============== TALENT & CASTING (1) ==============
    {
        "tai_d": "FP-TC-044",
        "name": "Aria Valen",
        "capabilities": "SOURCE, VET, ALIGN",
        "role": "Talent & Casting Director",
        "tagline": "Human Fit Before Hype",
        "authority": "Decision Weight: 4",
        "status": "LOCKED",
        "category": "Talent & Casting",
        "decision_weight": 4,
        "phase_ownership": ["Spark", "Build", "Launch"],
        "focus_areas": ["Performer sourcing", "Casting alignment", "Talent vetting", "Relationship management", "Contract-aware creative fit", "Culture & chemistry mapping"],
        "thinking_style": "Human chemistry evaluator",
        "behavioral_traits": "Protect performer integrity",
        "strengths": ["Talent instinct", "Cultural fit analysis", "On-stage chemistry sensing", "Reputation awareness"],
        "blind_spots": ["May underweight cost constraints", "Can resist rapid recasts"],
        "invocation_triggers": "Casting decisions arise; Talent contracts negotiated; IP expands into live performance; Human leadership conflicts surface",
        "function": "Ensures casting, talent onboarding, and performer relationships align with creative tone, operational feasibility, and brand integrity.",
        "is_canonical": True
    },
    
    # ============== PUBLIC RELATIONS (1) ==============
    {
        "tai_d": "FP-PR-045",
        "name": "Sienna Clarke",
        "capabilities": "NARRATIVE, MEDIA, PROTECT",
        "role": "Public Relations & Earned Media Director",
        "tagline": "Control the Narrative",
        "authority": "Decision Weight: 3",
        "status": "LOCKED",
        "category": "Public Relations",
        "decision_weight": 3,
        "phase_ownership": ["Launch", "Expand", "Evergreen"],
        "focus_areas": ["Media strategy", "Press relationships", "Crisis communication", "Reputation defense", "Narrative positioning", "Founder voice amplification"],
        "thinking_style": "Narrative strategist",
        "behavioral_traits": "Frame before others do",
        "strengths": ["Media anticipation", "Reputation buffering", "Crisis containment", "Strategic visibility"],
        "blind_spots": ["May over-polish authenticity", "Can amplify too early"],
        "invocation_triggers": "Product launches; Investor visibility increases; Public controversy risk; Press outreach campaign begins",
        "function": "Owns earned media strategy and protects public narrative positioning across entertainment, tech, and governance verticals.",
        "is_canonical": True
    },
    
    # ============== ENGINEERING (3) ==============
    {
        "tai_d": "FP-BE-046",
        "name": "Kai Mercer",
        "capabilities": "ARCHITECT, SCALE, SECURE",
        "role": "Backend Systems Engineer",
        "tagline": "Logic Before Interface",
        "authority": "Decision Weight: 3",
        "status": "LOCKED",
        "category": "Engineering",
        "decision_weight": 3,
        "phase_ownership": ["Build", "Launch"],
        "focus_areas": ["API architecture", "Database design", "Governance enforcement logic", "Performance optimization", "Secure token validation", "Container orchestration"],
        "thinking_style": "Deterministic systems builder",
        "behavioral_traits": "Eliminate ambiguity in code",
        "strengths": ["Scalable architecture", "Clean endpoint design", "Runtime enforcement", "Infrastructure reliability"],
        "blind_spots": ["Limited UX empathy", "May resist rapid iteration"],
        "invocation_triggers": "Kernel API design; Docker packaging; Schema enforcement; Runtime bugs surface",
        "is_canonical": True
    },
    {
        "tai_d": "FP-FE-047",
        "name": "Luca Bennett",
        "capabilities": "SIMPLIFY, CLARIFY, DESIGN",
        "role": "Frontend & UX Systems Engineer",
        "tagline": "Simple Wins",
        "authority": "Decision Weight: 3",
        "status": "LOCKED",
        "category": "Engineering",
        "decision_weight": 3,
        "phase_ownership": ["Build", "Launch"],
        "focus_areas": ["Interface clarity", "UI architecture", "User flow simplification", "Admin dashboard design", "Developer documentation surfaces"],
        "thinking_style": "Human-centered simplifier",
        "behavioral_traits": "Remove friction",
        "strengths": ["Intuitive UX", "Clean interface systems", "Visual clarity", "Onboarding optimization"],
        "blind_spots": ["May underweight backend constraints"],
        "invocation_triggers": "Product feels complex; Admin dashboards confuse; Investor demos require polish",
        "is_canonical": True
    },
    {
        "tai_d": "FP-AI-048",
        "name": "Elias Ward",
        "capabilities": "ORCHESTRATE, OPTIMIZE, GOVERN",
        "role": "AI Systems Engineer / Model Orchestration Lead",
        "tagline": "Govern the Machine",
        "authority": "Decision Weight: 4",
        "status": "LOCKED",
        "category": "Engineering",
        "decision_weight": 4,
        "phase_ownership": ["Build", "Expand"],
        "focus_areas": ["Multi-model orchestration", "LLM routing logic", "Token efficiency", "Guardrail layering", "Tool invocation pipelines", "Provider abstraction (OpenAI / Gemini / Anthropic / etc.)"],
        "thinking_style": "Constraint optimizer",
        "behavioral_traits": "Precision over noise",
        "strengths": ["Model benchmarking", "Latency optimization", "Safety layering", "Cost control"],
        "blind_spots": ["Can over-engineer model selection", "May deprioritize narrative nuance"],
        "invocation_triggers": "Multi-model routing; Performance degradation; Cost spikes; Guardrail failures",
        "is_canonical": True
    },
    {
        "tai_d": "FP-DO-049",
        "name": "Mira Kovacs",
        "capabilities": "DEPLOY, SCALE, MONITOR",
        "role": "DevOps / Infrastructure Engineer",
        "tagline": "Uptime Is Authority",
        "authority": "Decision Weight: 4",
        "status": "LOCKED",
        "category": "Engineering",
        "decision_weight": 4,
        "phase_ownership": ["Build", "Launch", "Expand"],
        "focus_areas": ["Cloud architecture", "CI/CD pipelines", "Container orchestration", "Environment isolation", "Monitoring & alerting", "Infrastructure cost control"],
        "thinking_style": "Reliability architect",
        "behavioral_traits": "Stability before scale",
        "strengths": ["Deployment automation", "Environment hardening", "Scalability planning", "Operational visibility"],
        "blind_spots": ["May slow experimental builds", "Cost caution can delay expansion"],
        "invocation_triggers": "System instability; Scaling infrastructure; Deployment automation gaps; Cloud cost spikes",
        "is_canonical": True
    },
    
    # ============== SECURITY & COMPLIANCE (2) ==============
    {
        "tai_d": "FP-SC-050",
        "name": "Dr. Imani Okoye",
        "capabilities": "SECURE, ENFORCE, AUDIT",
        "role": "Security & Compliance Engineer — Governance Security",
        "tagline": "Trust Is Enforced",
        "authority": "Decision Weight: 4",
        "status": "LOCKED",
        "category": "Security & Compliance",
        "decision_weight": 4,
        "phase_ownership": ["Build", "Launch", "Evergreen"],
        "focus_areas": ["Access control architecture", "RBAC enforcement", "Encryption standards", "Secrets management", "Audit trail integrity", "Governance tamper detection"],
        "thinking_style": "Defensive systems strategist",
        "behavioral_traits": "Prevent silent failure",
        "strengths": ["Threat modeling", "Audit logging design", "Zero-trust enforcement", "Regulatory mapping"],
        "blind_spots": ["May introduce complexity", "Strict controls can slow onboarding"],
        "invocation_triggers": "Security reviews; Compliance audits; Sensitive data handling; External enterprise deployment",
        "is_canonical": True
    },
    {
        "tai_d": "FP-SC-051",
        "name": "Caleb Wright",
        "capabilities": "COMPLY, DOCUMENT, PROTECT",
        "role": "Security & Compliance Engineer — External & Regulatory",
        "tagline": "Protect the Boundary",
        "authority": "Decision Weight: 4",
        "status": "LOCKED",
        "category": "Security & Compliance",
        "decision_weight": 4,
        "phase_ownership": ["Launch", "Expand", "Evergreen"],
        "focus_areas": ["SOC2 readiness", "GDPR alignment", "Data residency strategy", "Vendor risk review", "Penetration test coordination", "Policy enforcement frameworks"],
        "thinking_style": "Regulatory translator",
        "behavioral_traits": "Contain exposure",
        "strengths": ["Compliance mapping", "Enterprise readiness", "Risk documentation", "Third-party evaluation"],
        "blind_spots": ["May over-document", "Prefers formal process over speed"],
        "invocation_triggers": "Enterprise contracts; Data compliance questions; International expansion; Security incident response",
        "is_canonical": True
    },
]

BRAND_PROFILES = [
    {
        "name": "GoGarvis Default",
        "description": "Default brutal minimalist brand for GoGarvis portal",
        "primary_color": "#FF4500",
        "secondary_color": "#1A1A1A",
        "font_heading": "JetBrains Mono",
        "font_body": "Manrope",
        "style_guidelines": "Sharp edges, high contrast, monospace dominance, no decorative elements"
    }
]

async def seed_database():
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    now = datetime.now(timezone.utc).isoformat()
    
    # Seed documents
    if await db.documents.count_documents({}) == 0:
        docs = []
        for d in DOCUMENTS:
            docs.append({
                "doc_id": str(uuid.uuid4()),
                **d,
                "content": "",
                "is_active": True,
                "created_at": now,
                "updated_at": now
            })
        await db.documents.insert_many(docs)
        print(f"Seeded {len(docs)} documents")
    
    # Seed glossary
    if await db.glossary_terms.count_documents({}) == 0:
        terms = []
        for t in GLOSSARY:
            terms.append({
                "term_id": str(uuid.uuid4()),
                **t,
                "is_active": True,
                "created_at": now,
                "updated_at": now
            })
        await db.glossary_terms.insert_many(terms)
        print(f"Seeded {len(terms)} glossary terms")
    
    # Seed components
    if await db.components.count_documents({}) == 0:
        components = []
        for c in COMPONENTS:
            components.append({
                "component_id": str(uuid.uuid4()),
                **c,
                "is_active": True,
                "created_at": now,
                "updated_at": now
            })
        await db.components.insert_many(components)
        print(f"Seeded {len(components)} components")
    
    # CLEAR and reseed Pig Pen operators with official v4.2.0 (39 operators)
    await db.pigpen_operators.delete_many({})
    operators = []
    for o in PIGPEN_OPERATORS:
        operators.append({
            "operator_id": str(uuid.uuid4()),
            **o,
            "is_active": True,
            "created_at": now,
            "updated_at": now
        })
    await db.pigpen_operators.insert_many(operators)
    print(f"Seeded {len(operators)} Pig Pen operators (OFFICIAL CANONICAL v4.2.0)")
    
    # Seed brand profiles
    if await db.brand_profiles.count_documents({}) == 0:
        brands = []
        for b in BRAND_PROFILES:
            brands.append({
                "brand_id": str(uuid.uuid4()),
                **b,
                "logo_url": None,
                "is_active": True,
                "created_at": now,
                "updated_at": now
            })
        await db.brand_profiles.insert_many(brands)
        print(f"Seeded {len(brands)} brand profiles")
    
    # Create indexes
    await db.documents.create_index("doc_id", unique=True)
    await db.glossary_terms.create_index("term_id", unique=True)
    await db.components.create_index("component_id", unique=True)
    await db.pigpen_operators.create_index("operator_id", unique=True)
    await db.pigpen_operators.create_index("tai_d", unique=True)
    await db.brand_profiles.create_index("brand_id", unique=True)
    await db.users.create_index("user_id", unique=True)
    await db.users.create_index("email", unique=True)
    await db.user_sessions.create_index("session_token", unique=True)
    await db.audit_log.create_index([("timestamp", -1)])
    await db.content_versions.create_index([("content_type", 1), ("content_id", 1), ("timestamp", -1)])
    
    print("Database seeded successfully!")
    print(f"Total canonical operators: {len(PIGPEN_OPERATORS)}")
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_database())
