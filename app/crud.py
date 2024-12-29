from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import Item
from schemas import ItemCreate
from geoalchemy2 import WKTElement
from geoalchemy2.shape import to_shape



async def create_item(db: AsyncSession, item: ItemCreate):
    db_item = Item(name=item.name, description=item.description, geom=WKTElement(item.geom, srid=4326) )
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return {"status": 201,"message":'Added successfully'}

async def get_items(db: AsyncSession):
    result = await db.execute(select(Item))
    items = result.scalars().all()
    for obj in items:
        if isinstance(obj.geom, str):
            obj.geom = WKTElement(obj.geom)
        obj.geom = to_shape(obj.geom).wkt
    return  items

