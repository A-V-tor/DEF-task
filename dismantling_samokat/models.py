from itertools import product
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import (
    Integer,
    String,
    Column,
    DECIMAL,
    DateTime,
    Boolean,
    Text,
    JSON,
    Enum,
    desc,
    event,
)


class Base(DeclarativeBase):
    pass


class MainLinks(Base):
    """Хранение ссылок с главной страницы"""

    __tablename__ = 'mainlinks'
    id = Column(Integer, primary_key=True)
    id_site = Column(String)
    name = Column(String)
    rank = Column(Integer)
    image = Column(String)
    parentId = Column(String)
    link = Column(String)


class ProductsFamilie(Base):
    __tablename__ = 'productsfamilie'
    id = Column(Integer, primary_key=True)
    id_site = Column(String, unique=True)
    name = Column(String)
    rank = Column(Integer)
    productIds = Column(JSON)
    parentId = Column(String)
    link = Column(String)


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    weight = Column(String)
    abstract_description = Column(String)
    description = Column(String)
    compound = Column(String)
    shelf_life = Column(String)
    storage_conditions = Column(String)
    manufacturer = Column(String)
    price = Column(String)
    nutr = Column(String)
    image = Column(String)
    link = Column(String)
