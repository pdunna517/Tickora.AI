from typing import Any
from sqlalchemy.ext.declarative import as_declarative, declared_attr

@as_declarative()
class Base:
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

# Import all models here for Alembic
# Note: This is a bit circular if models import Base, so we usually rely on 
# env.py importing the models explicitly or a central models/__init__.py
