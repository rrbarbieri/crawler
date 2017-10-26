import enum
from sqlalchemy import (Column, Integer, String)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_enum34 import EnumType

Base = declarative_base()


class Status(enum.Enum):
    new = 'new'
    visited = 'visited'
    error = 'error'


# declare Link database table
class Link(Base):
    __tablename__ = 'link'

    depth = Column(Integer, primary_key=True)
    url = Column(String(1022), primary_key=True)
    status = Column(EnumType(Status, name='url_status'), nullable=False, default=Status.new, index=True)

    def __init__(self, url, depth=1, status=Status.new):
        self.url = url
        self.depth = depth
        self.status = status


# declare Product database table
class Product(Base):
    __tablename__ = 'product'

    url = Column(String(1022), primary_key=True)
    title = Column(String(256), nullable=False)
    name = Column(String(256), nullable=False)

    def __init__(self, url, title, name):
        self.url = url
        self.title = title
        self.name = name
