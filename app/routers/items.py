from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from schemas import Item, ItemCreate
from crud import create_item, get_items

router = APIRouter()

@router.post("/")
async def create_new_item(item: ItemCreate, db: AsyncSession = Depends(get_db)):
    res = await create_item(db, item)
    return res

@router.get("/")
async def read_items(db: AsyncSession = Depends(get_db)):
    return await get_items(db)