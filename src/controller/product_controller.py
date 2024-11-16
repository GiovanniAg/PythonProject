

from typing import Optional
from models.product_model import ProductModel
from repositories.product_repository import ProductRepository
from schemas.ProductSchema import ProductCreateSchemaBase, ProductUpdateSchemaBase
from sanic.exceptions import SanicException
from sqlalchemy.exc import IntegrityError


class ProductController:

    def __init__(self):
        self.product_repository = ProductRepository()
    
    def list_products(self, filters: Optional[dict], sort_by: Optional[str]) -> list[ProductModel]:
        return self.product_repository.list(filters, sort_by)
    
    def create_product(self, product: ProductCreateSchemaBase) -> ProductModel:
        try:
            product_model = ProductModel(**product.model_dump())
            return self.product_repository.create(product_model)
        except IntegrityError as ex:
            print(ex)
            raise SanicException("Já existe um produto com esse nome", 409)
    
    def update_product(self, product_id: int, product_values: ProductUpdateSchemaBase) -> ProductModel:
        product = self.product_repository.find(product_id)

        if not product:
            raise SanicException("Produto não encontrado", 404)
        
        try:
            values_to_update = ProductModel(**product_values.model_dump())
            return self.product_repository.update(product, values_to_update)
        except IntegrityError:
            raise SanicException("Já existe um produto com esse nome", 409)
    
    def delete_product(self, product_id: int) -> None:
        product = self.product_repository.find(product_id)

        if not product:
            raise SanicException("Produto não encontrado", 404)
        
        self.product_repository.delete(product)