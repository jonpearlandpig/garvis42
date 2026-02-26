# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.governance import router as governance_router
from persistence import PersistenceLayer, get_persistence_layer
from policy import initialize_stores

app = FastAPI(
    title="GARVIS Governance PoC",
    description="Proof of Concept for Garvis Governance Layer with CAC and Dual LLMs.",
    version="0.1.0",
)

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://your-vercel-deployment-url.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

initialize_stores()
PERSISTENCE = PersistenceLayer(db_path="garvis_governance.db")
PERSISTENCE.connect()

app.include_router(governance_router)

@app.get("/")
async def read_root():
    return {"message": "GARVIS Governance PoC Backend is running!"}

@app.on_event("shutdown")
def shutdown_event():
    PERSISTENCE.close()
    print("Shutdown complete.")
