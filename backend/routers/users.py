from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/")
async def get_all_users():
    return [{"id": 1, "username": "alice"}, {"id": 2, "username": "bob"}]

@router.get("/{user_id}")
async def get_user_by_id(user_id: int):
    return {"id": user_id, "username": f"user{user_id}"}
