from sqlalchemy import Column, Integer, Text, Float, DateTime
from config.database import Base


class ProductModel(Base):

    __tablename__ = "product"

    id            = Column(Integer, primary_key=True, autoincrement=True)
    name          = Column(Text, nullable=False, unique=True)
    description   = Column(Text, nullable=False)
    price         = Column(Float, nullable=False)
    inventory     = Column(Integer, nullable=False)
    category      = Column(Text, nullable=False)
    created_at    = Column(DateTime, nullable=False)
    updated_at    = Column(DateTime, nullable=False)

    def dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'inventory': self.inventory,
            'category': self.category,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
