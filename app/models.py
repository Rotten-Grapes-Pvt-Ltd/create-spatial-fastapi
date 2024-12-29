from sqlalchemy import Column, Integer, String
from geoalchemy2 import Geometry
from database import Base
class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    geom = Column(Geometry("POINT"))