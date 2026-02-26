from fastapi import APIRouter, HTTPException
from typing import List
from backend.models import Item, ItemCreate

router = APIRouter(prefix="/items", tags=["Items"])

@router.get("/", response_model=List[Item])
async def get_all_items() -> List[Item]:
    """
    Retrieves a list of all available items.

    This endpoint fetches all items from the database and returns them.
    Useful for displaying catalogs or overviews.
    """
    return [
        Item(id=1, name="Sample Item", description="A demo item."),
        Item(id=2, name="Another Item", description="Another demo item.")
    ]

@router.post("/", response_model=Item, status_code=201)
async def create_new_item(item: ItemCreate) -> Item:
    """
    Creates a new item.

    Accepts item details in the request body and returns the created item
    with its assigned ID.
    """
    new_item_data = Item(id=99, **item.dict())
    return new_item_data

@router.get("/{item_id}", response_model=Item)
async def get_item_by_id(item_id: int) -> Item:
    """
    Retrieves a specific item by its unique ID.
    """
    return Item(id=item_id, name=f"Item {item_id}", description="Fetched by ID.")
