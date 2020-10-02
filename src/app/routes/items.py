from typing import List

from fastapi import APIRouter
from app.schemas.item import Item, ItemCreate, ItemUpdate

router = APIRouter()

an_item = {"id": 1, "title": "Thing", "description": "A thing", "owner_id": 7}
another = {"id": 2, "title": "Stuff", "description": "Some stuff", "owner_id": 3}


@router.get("/", response_model=List[Item])
def read_items():
    """
    Retrieve items.
    """
    return [an_item, another]


@router.post("/", response_model=Item)
def create_item(*, item_in: ItemCreate):
    """
    Create new item.
    """
    item = {"id": 3, "owner_id": 1}
    item.update(item_in)
    return item


@router.put("/{id}", response_model=Item)
def update_item(*, id: int, item_in: ItemUpdate):
    """
    Update an item.
    """
    an_item.update(id=id)
    an_item.update(item_in)
    return an_item


@router.get("/{id}", response_model=Item)
def read_item(*, id: int):
    """
    Get item by ID.
    """
    an_item.update(id=id)
    return an_item


@router.delete("/{id}", response_model=Item)
def delete_item(*, id: int):
    """
    Delete an item.
    """
    an_item.update(id=id)
    return an_item
