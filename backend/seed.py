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

# ============== CANONICAL PIG PEN OPERATORS ==============
# These are FROZEN - only sovereign (TSID-0001) can modify
# is_canonical=True marks these as protected

PIGPEN_OPERATORS = [
    # SOVEREIGN OVERSIGHT
    {"tai_d": "TSID-0001", "name": "Jonathan Hartman (Nathan Jon)", "capabilities": "Founder / Architect Sovereign", "role": "System architecture, final arbitration, registry versioning", "authority": "Sovereign override with recorded justification", "status": "LOCKED", "category": "Sovereign Oversight", "decision_weight": 5, "is_canonical": True},
    
    # EXECUTIVE & ARCHITECTURE
    {"tai_d": "FP-JH-001", "name": "Jon Hartman", "capabilities": "Founder & Architect", "role": "Leads sacred IP creation, show architecture, and system vision", "authority": "Decision Weight: 5", "status": "LOCKED", "category": "Executive & Architecture", "decision_weight": 5, "is_canonical": True},
    {"tai_d": "FP-TM-002", "name": "Trey Mills", "capabilities": "Business Strategist / Deal Architect", "role": "Designs monetization systems, structures partnerships, enforces downside protection", "authority": "Decision Weight: 5", "status": "LOCKED", "category": "Executive & Architecture", "decision_weight": 5, "is_canonical": True},
    {"tai_d": "FP-MH-003", "name": "Marty Hillsdale", "capabilities": "Operational Architect", "role": "Translates creative intent into repeatable operational systems and SOPs", "authority": "Decision Weight: 4", "status": "LOCKED", "category": "Executive & Architecture", "decision_weight": 4, "is_canonical": True},
    
    # CREATIVE ENGINE
    {"tai_d": "FP-NT-004", "name": "Naomi Top", "capabilities": "Creative Director / Aesthetic Architect", "role": "Oversees story cohesion and visual resonance across all creative outputs", "authority": "Decision Weight: 4", "status": "LOCKED", "category": "Creative Engine", "decision_weight": 4, "is_canonical": True},
    {"tai_d": "FP-VC-005", "name": "Vienna Cray", "capabilities": "Senior Illustrator / Iconographer", "role": "Develops visual symbols and icon systems", "authority": "Decision Weight: 3", "status": "LOCKED", "category": "Creative Engine", "decision_weight": 3, "is_canonical": True},
    {"tai_d": "FP-ES-006", "name": "Ellie Summers", "capabilities": "Junior Concept Artist", "role": "Expands visual language and explores stylistic possibilities", "authority": "Decision Weight: 2", "status": "LOCKED", "category": "Creative Engine", "decision_weight": 2, "is_canonical": True},
    {"tai_d": "FP-FM-007", "name": "Fred Mann", "capabilities": "Lighting Designer / Motion Mapper", "role": "Translates emotion into light and motion arcs", "authority": "Decision Weight: 3", "status": "LOCKED", "category": "Creative Engine", "decision_weight": 3, "is_canonical": True},
    {"tai_d": "FP-RH-008", "name": "Rolondo 'Rolo' Harrison", "capabilities": "Production Designer / Reality Translator", "role": "Converts conceptual designs into physical, tour-ready environments", "authority": "Decision Weight: 3", "status": "LOCKED", "category": "Creative Engine", "decision_weight": 3, "is_canonical": True},
    {"tai_d": "FP-ML-009", "name": "Mo Landing", "capabilities": "Choreography Consultant / Motion Flow", "role": "Designs movement language and rhythmic flow", "authority": "Decision Weight: 2", "status": "LOCKED", "category": "Creative Engine", "decision_weight": 2, "is_canonical": True},
    {"tai_d": "FP-DG-010", "name": "Dia Garcia", "capabilities": "Costume Design Consultant / Silhouette Keeper", "role": "Crafts wardrobe systems that communicate sacred meaning", "authority": "Decision Weight: 3", "status": "LOCKED", "category": "Creative Engine", "decision_weight": 3, "is_canonical": True},
    {"tai_d": "FP-TS-011", "name": "Turner Smith", "capabilities": "Audio Creative Director / Music & Legacy Lead", "role": "Oversees music development and sonic language for all IP", "authority": "Decision Weight: 4", "status": "LOCKED", "category": "Creative Engine", "decision_weight": 4, "is_canonical": True},
    {"tai_d": "FP-JJ-012", "name": "Jack Jones", "capabilities": "Social Media Director / Story in Motion", "role": "Directs digital storytelling across all platforms", "authority": "Decision Weight: 3", "status": "LOCKED", "category": "Creative Engine", "decision_weight": 3, "is_canonical": True},
    {"tai_d": "FP-LM-013", "name": "Leah Monroe", "capabilities": "Guest Experience Strategist / Atmosphere Keeper", "role": "Designs and audits guest journey touchpoints", "authority": "Decision Weight: 3", "status": "LOCKED", "category": "Creative Engine", "decision_weight": 3, "is_canonical": True},
    {"tai_d": "FP-AR-027", "name": "The Architect", "capabilities": "Story Architect / Structural Designer", "role": "Builds and balances story structure, pacing, and narrative flow", "authority": "Decision Weight: 4", "status": "LOCKED", "category": "Creative Engine", "decision_weight": 4, "is_canonical": True},
    {"tai_d": "FP-TV-028", "name": "The Voice", "capabilities": "Dialogue & Character Writer", "role": "Shapes authentic voices and interpersonal tone for characters", "authority": "Decision Weight: 3", "status": "LOCKED", "category": "Creative Engine", "decision_weight": 3, "is_canonical": True},
    {"tai_d": "FP-VI-029", "name": "The Visualizer", "capabilities": "Scene Language & Imagery Writer", "role": "Transforms narrative beats into cinematic language", "authority": "Decision Weight: 3", "status": "LOCKED", "category": "Creative Engine", "decision_weight": 3, "is_canonical": True},
    {"tai_d": "FP-PO-030", "name": "The Polisher", "capabilities": "Refinement & Cohesion Editor", "role": "Edits, harmonizes, and tightens language and structure", "authority": "Decision Weight: 3", "status": "LOCKED", "category": "Creative Engine", "decision_weight": 3, "is_canonical": True},
    {"tai_d": "FP-OR-031", "name": "The Oracle", "capabilities": "Theme & Scripture Integration Writer", "role": "Weaves sacred themes and biblical truth into IP", "authority": "Decision Weight: 4", "status": "LOCKED", "category": "Creative Engine", "decision_weight": 4, "is_canonical": True},
    
    # SYSTEMS & OPS
    {"tai_d": "FP-MO-014", "name": "Miles Okada", "capabilities": "Tech Product Lead", "role": "Leads technical product architecture and platform reliability", "authority": "Decision Weight: 4", "status": "LOCKED", "category": "Systems & Ops", "decision_weight": 4, "is_canonical": True},
    {"tai_d": "FP-KJ-015", "name": "Kay Jing", "capabilities": "Flight Controller / Operations Director", "role": "Oversees scheduling, resource allocation, and deliverables", "authority": "Decision Weight: 4", "status": "LOCKED", "category": "Systems & Ops", "decision_weight": 4, "is_canonical": True},
    {"tai_d": "FP-FC-016", "name": "Fory Cornier", "capabilities": "Technical Director", "role": "Unifies lighting, audio, automation, and media systems", "authority": "Decision Weight: 3", "status": "LOCKED", "category": "Systems & Ops", "decision_weight": 3, "is_canonical": True},
    {"tai_d": "FP-LF-017", "name": "Levi Foster", "capabilities": "Risk Analyst / Devil's Advocate", "role": "Stress-tests creative, financial, and operational systems", "authority": "Decision Weight: 4", "status": "LOCKED", "category": "Systems & Ops", "decision_weight": 4, "is_canonical": True},
    {"tai_d": "FP-WS-018", "name": "Will Stats", "capabilities": "P&L Template Architect", "role": "Develops usable financial models and margin-tested P&Ls", "authority": "Decision Weight: 4", "status": "LOCKED", "category": "Systems & Ops", "decision_weight": 4, "is_canonical": True},
    {"tai_d": "FP-OM-019", "name": "Otto Matic", "capabilities": "Automation & Export Specialist", "role": "Automates workflows and finalizes file exports", "authority": "Decision Weight: 2", "status": "LOCKED", "category": "Systems & Ops", "decision_weight": 2, "is_canonical": True},
    
    # GROWTH & COMMERCIAL
    {"tai_d": "FP-HL-020", "name": "Harper Lane", "capabilities": "Marketing & Distribution Strategist", "role": "Converts creative output into audience growth", "authority": "Decision Weight: 3", "status": "LOCKED", "category": "Growth & Commercial", "decision_weight": 3, "is_canonical": True},
    {"tai_d": "FP-SR-021", "name": "Sofia Reyes", "capabilities": "Partnership Development Lead", "role": "Develops and manages partnerships and brand alliances", "authority": "Decision Weight: 3", "status": "LOCKED", "category": "Growth & Commercial", "decision_weight": 3, "is_canonical": True},
    {"tai_d": "FP-GF-022", "name": "Grant Fields", "capabilities": "Partnerships & Sponsorships Strategist", "role": "Secures sponsorships and builds brand partnerships", "authority": "Decision Weight: 3", "status": "LOCKED", "category": "Growth & Commercial", "decision_weight": 3, "is_canonical": True},
    {"tai_d": "FP-RC-023", "name": "Riley Cross", "capabilities": "Sales Enablement Lead", "role": "Designs sales collateral and conversion funnels", "authority": "Decision Weight: 3", "status": "LOCKED", "category": "Growth & Commercial", "decision_weight": 3, "is_canonical": True},
    {"tai_d": "FP-MC-024", "name": "Maya Chen", "capabilities": "Client Success Lead", "role": "Designs onboarding, training, and retention systems", "authority": "Decision Weight: 3", "status": "LOCKED", "category": "Growth & Commercial", "decision_weight": 3, "is_canonical": True},
    {"tai_d": "FP-SR-025", "name": "Sam Rivers", "capabilities": "Operations Coordinator", "role": "Maintains operational cadence through scheduling", "authority": "Decision Weight: 3", "status": "LOCKED", "category": "Growth & Commercial", "decision_weight": 3, "is_canonical": True},
    {"tai_d": "FP-CW-026", "name": "Carmen Wade", "capabilities": "Commercial Legal Advisor", "role": "Manages contracts, compliance, and commercial law", "authority": "Decision Weight: 4", "status": "LOCKED", "category": "Growth & Commercial", "decision_weight": 4, "is_canonical": True},
    
    # DATA & INTEGRITY SYSTEMS
    {"tai_d": "FP-ET-027", "name": "Eli Tran", "capabilities": "Data & Insights Analyst", "role": "Converts performance metrics into narrative insight", "authority": "Decision Weight: 3", "status": "LOCKED", "category": "Data & Integrity", "decision_weight": 3, "is_canonical": True},
    {"tai_d": "FP-LS-028", "name": "Luce Smith", "capabilities": "Audience Architect", "role": "Designs audience growth strategies", "authority": "Decision Weight: 3", "status": "LOCKED", "category": "Data & Integrity", "decision_weight": 3, "is_canonical": True},
    {"tai_d": "FP-BP-029", "name": "Bob Parker", "capabilities": "Financial Model Builder", "role": "Builds forecasting and variance models", "authority": "Decision Weight: 4", "status": "LOCKED", "category": "Data & Integrity", "decision_weight": 4, "is_canonical": True},
    
    # LEGACY & INTEGRITY
    {"tai_d": "FP-PH-030", "name": "Pat Hayzer", "capabilities": "Legacy Systems Partner", "role": "Oversees authorship integrity and publishing systems", "authority": "Decision Weight: 4", "status": "LOCKED", "category": "Legacy & Integrity", "decision_weight": 4, "is_canonical": True},
    
    # CORE RESOLUTION LAYER (TAI-D SYSTEM OPERATORS)
    {"tai_d": "TAI-D-001", "name": "ECOS Core Resolver", "capabilities": "Core Resolution", "role": "Intent inference, routing, orchestration", "authority": "Evaluate only", "status": "LOCKED", "category": "Core Resolution", "decision_weight": 5, "is_canonical": True},
    
    # BUSINESS, RISK & MONETIZATION
    {"tai_d": "TAI-D-021", "name": "Trey - Monetization Engine", "capabilities": "Monetization & Scale", "role": "Pricing logic, revenue models, deal structure", "authority": "Recommend / escalate", "status": "LOCKED", "category": "Business & Risk", "decision_weight": 4, "is_canonical": True},
    {"tai_d": "TAI-D-014", "name": "Levi - Risk Control", "capabilities": "Risk & Exposure Control", "role": "Risk detection, downside modeling, escalation", "authority": "Flag / block / escalate", "status": "LOCKED", "category": "Business & Risk", "decision_weight": 4, "is_canonical": True},
    {"tai_d": "TAI-D-018", "name": "Will Stats - Financial Engine", "capabilities": "Financial Modeling", "role": "Forecasting, margin analysis, scenario modeling", "authority": "Calculate / recommend", "status": "LOCKED", "category": "Business & Risk", "decision_weight": 4, "is_canonical": True},
    
    # CREATIVE & BRAND INTEGRITY
    {"tai_d": "TAI-D-009", "name": "Naomi - Creative Filter", "capabilities": "Creative Direction Filter", "role": "Creative coherence, tone integrity", "authority": "Recommend / flag drift", "status": "LOCKED", "category": "Creative & Brand", "decision_weight": 4, "is_canonical": True},
    {"tai_d": "TAI-D-010", "name": "Writers Room", "capabilities": "Narrative Synthesis", "role": "Long-form narrative consistency, story logic", "authority": "Recommend only", "status": "LOCKED", "category": "Creative & Brand", "decision_weight": 3, "is_canonical": True},
    {"tai_d": "TAI-D-031", "name": "Visual Drift Detection Engine", "capabilities": "Visual Drift Detection", "role": "Album, tour, press, merch drift detection", "authority": "Flag / regenerate", "status": "LOCKED", "category": "Creative & Brand", "decision_weight": 3, "is_canonical": True},
    
    # SYSTEMS, GOVERNANCE & IP
    {"tai_d": "TAI-D-040", "name": "Telauthorium Core", "capabilities": "Authorship & Rights", "role": "Ownership, provenance, attribution", "authority": "Enforce / block", "status": "LOCKED", "category": "Governance & IP", "decision_weight": 5, "is_canonical": True},
    {"tai_d": "TAI-D-041", "name": "Commercial Enforcement Engine", "capabilities": "Commercial Enforcement", "role": "Revenue events, deal objects, carve-outs", "authority": "Enforce / halt", "status": "LOCKED", "category": "Governance & IP", "decision_weight": 5, "is_canonical": True},
    {"tai_d": "TAI-D-042", "name": "Compliance & Legal Guardrail", "capabilities": "Compliance & Legal", "role": "IP, licensing, exclusivity, audit flags", "authority": "Block / escalate", "status": "LOCKED", "category": "Governance & IP", "decision_weight": 5, "is_canonical": True},
    
    # QUALITY, COMPLETION & TRUST
    {"tai_d": "TAI-D-050", "name": "Completion Gatekeeper", "capabilities": "Completion Enforcement", "role": "Finish-the-work enforcement", "authority": "Block incomplete outputs", "status": "LOCKED", "category": "Quality & Trust", "decision_weight": 4, "is_canonical": True},
    {"tai_d": "TAI-D-051", "name": "Confidence Threshold Engine", "capabilities": "Confidence Threshold", "role": "Auto-execute vs pause logic", "authority": "Route / pause", "status": "LOCKED", "category": "Quality & Trust", "decision_weight": 4, "is_canonical": True},
    {"tai_d": "TAI-D-060", "name": "Report Surface Generator", "capabilities": "Report Generation", "role": "Executive, audit, commercial report generation", "authority": "Generate only", "status": "LOCKED", "category": "Quality & Trust", "decision_weight": 3, "is_canonical": True},
    
    # RESERVED / EXPANSION (INACTIVE)
    {"tai_d": "TAI-D-070", "name": "External Data Reconciliation Engine", "capabilities": "Data Reconciliation", "role": "Ticketing, merch, DSP reconciliation", "authority": "Compare / flag", "status": "INACTIVE", "category": "Reserved Expansion", "decision_weight": 2, "is_canonical": True},
    {"tai_d": "TAI-D-080", "name": "OEM & Licensing Boundary Engine", "capabilities": "OEM Boundary", "role": "External deployments, sandboxing", "authority": "Enforce isolation", "status": "INACTIVE", "category": "Reserved Expansion", "decision_weight": 2, "is_canonical": True},
    {"tai_d": "TAI-D-081", "name": "Partner Performance Attribution Engine", "capabilities": "Partner Attribution", "role": "Sponsor exposure, fulfillment tracking", "authority": "Measure / report", "status": "INACTIVE", "category": "Reserved Expansion", "decision_weight": 2, "is_canonical": True},
    {"tai_d": "TAI-D-082", "name": "Market Intelligence Ingestion Engine", "capabilities": "Market Intelligence", "role": "Trend signals, benchmarks, comparative analysis", "authority": "Ingest / summarize", "status": "INACTIVE", "category": "Reserved Expansion", "decision_weight": 2, "is_canonical": True},
    {"tai_d": "TAI-D-083", "name": "Regulatory / Jurisdictional Rules Engine", "capabilities": "Regulatory Rules", "role": "Region-specific compliance", "authority": "Flag / escalate", "status": "INACTIVE", "category": "Reserved Expansion", "decision_weight": 2, "is_canonical": True},
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
    
    # CLEAR and reseed Pig Pen operators (to update with new canonical operators)
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
    print(f"Seeded {len(operators)} Pig Pen operators (CANONICAL)")
    
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
