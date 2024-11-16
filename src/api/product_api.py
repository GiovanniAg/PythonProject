from sanic import Blueprint, Request
from sanic.response import JSONResponse
from sanic_ext import openapi

from controller.product_controller import ProductController
from schemas.ProductSchema import ProductCreateSchemaBase, ProductSchemaBase, ProductUpdateSchemaBase

blueprint = Blueprint("products")


@blueprint.get("/", name='List products')
@openapi.parameter('name', str, "query")
@openapi.parameter('description', str, "query")
@openapi.parameter('price', float, "query")
@openapi.parameter('inventory', int, "query")
@openapi.response(200, {"application/json": ProductSchemaBase.model_json_schema()}, "Success")
def list_products(req: Request):

    allowed_str_query_args = ["name", "description",]
    allowed_num_query_args = ["price", "inventory"]

    query = req.get_query_args()
    filters = {}
    sort_by = None

    for query_arg in query:
        if query_arg[0] in allowed_str_query_args:
            filters[query_arg[0]] = query_arg[1]
        if query_arg[0] in allowed_num_query_args:
            filters[query_arg[0]] = float(query_arg[1])
        if query_arg[0] == "sort":
            sort_by = query_arg[1]

    controller = ProductController()
    result =  controller.list_products(filters, sort_by)
    return JSONResponse([product.dict() for product in result], 200)


@blueprint.post("/", name='Insert product')
@openapi.body(
    content={"application/json": ProductCreateSchemaBase.model_json_schema()},
    required=True
)
@openapi.response(200, {"application/json": ProductSchemaBase.model_json_schema()}, "Success")
@openapi.response(404, {"text/plain": "Produto não encontrado"}, "Not found")
@openapi.response(409, {"text/plain": "Já existe um produto com esse nome"}, "Conflict")
async def insert_product(req: Request):
    body = req.json
    controller = ProductController()
    product_to_create = ProductCreateSchemaBase(**body)
    result =  controller.create_product(product_to_create)
    return JSONResponse(result.dict(), 200)


@blueprint.put("/<id>", name='Update product')
@openapi.body(
    content={"application/json": ProductUpdateSchemaBase.model_json_schema()},
    required=True
)
@openapi.response(200, {"application/json": ProductSchemaBase.model_json_schema()})
@openapi.response(404, {"text/plain": "Produto não encontrado"}, "Not found")
@openapi.response(409, {"text/plain": "Já existe um produto com esse nome"}, "Conflict")
def update_product(req: Request, id: int):
    body = req.json
    controller = ProductController()
    values_to_update = ProductUpdateSchemaBase(**body)
    result =  controller.update_product(id, values_to_update)
    return JSONResponse(result.dict(), 200)


@blueprint.delete("/<id>", name='Delete product')
@openapi.response(200, None, "Success")
@openapi.response(404, {"text/plain": "Produto não encontrado"}, "Not found")
@openapi.response(409, {"text/plain": "Já existe um produto com esse nome"}, "Conflict")
async def delete_product(req: Request, id: int):
    controller = ProductController()
    controller.delete_product(id)
    return JSONResponse(status=200)