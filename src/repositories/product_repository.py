from datetime import datetime
from typing import Optional
from sqlalchemy import select, func
from config.database import Session
from models.product_model import ProductModel

class ProductRepository:

    def __init__(self) -> None:
        self.session = Session()
    
    def list(self, filters: Optional[dict] = None, sort_by: Optional[str] = None) -> list[ProductModel]:

        query = select(ProductModel)

        if filters:
            for filter_key in filters.keys():
                filter_value = filters[filter_key]
                if isinstance(filter_value, str):
                    query = query.filter(func.lower(getattr(ProductModel, filter_key)).contains(filter_value.lower()))
                else:
                    query = query.filter(getattr(ProductModel, filter_key) == filter_value)
        
        if sort_by:
            query = query.order_by(getattr(ProductModel, sort_by))
        else:
            query = query.order_by(ProductModel.name)

        result = self.session.execute(query)
        products: list[ProductModel] = result.scalars().all()
        return products
    
    def find(self, id: int) -> Optional[ProductModel]:
        query = select(ProductModel).filter(ProductModel.id == id)
        result = self.session.execute(query)
        product: Optional[ProductModel] = result.scalars().unique().one_or_none()
        return product
    
    def create(self, product: ProductModel) -> ProductModel:
        product.created_at = datetime.now()
        product.updated_at = datetime.now()
        self.session.add(product)
        self.session.commit()
        self.session.refresh(product)
        return product
    
    def update(self, product: ProductModel, values_to_update: ProductModel) -> ProductModel:
        if values_to_update.name:
            product.name = values_to_update.name
        if values_to_update.description:
            product.description = values_to_update.description
        if values_to_update.price:
            product.price = values_to_update.price
        if values_to_update.inventory:
            product.inventory = values_to_update.inventory
        if values_to_update.category:
            product.category = values_to_update.category
        
        product.updated_at = datetime.now()

        self.session.commit()
        self.session.refresh(product)

        return product
    
    def delete(self, product: ProductModel) -> None:
        self.session.delete(product)
        self.session.commit()
