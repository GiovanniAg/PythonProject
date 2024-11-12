from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class ProductSchemaBase(BaseModel):

    id: int
    name: str
    description: str
    price: float
    inventory: int
    category: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class ProductCreateSchemaBase(BaseModel):

    name: str
    description: str
    price: float
    inventory: int
    category: str


class ProductUpdateSchemaBase(BaseModel):

    name: Optional[str] = None
    description: Optional[str]  = None
    price: Optional[float] = None
    inventory: Optional[int] = None
    category: Optional[str] = None
