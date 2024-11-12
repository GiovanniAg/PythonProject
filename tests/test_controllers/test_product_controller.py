
import copy
import pytest
from sanic import SanicException
from sqlalchemy.exc import IntegrityError

from controller.product_controller import ProductController
from schemas.ProductSchema import ProductCreateSchemaBase, ProductUpdateSchemaBase

ERROR_404_MESSAGE = "Produto não encontrado"
ERROR_409_MESSAGE = "Já existe um produto com esse nome"

# region List Products

def test_list_product_success(mock_db_session, helpers):

    result_length = 10
    product_model_list = [helpers.generate_random_product() for _ in range(result_length)]
    mock_db_session.list.return_value = copy.deepcopy(product_model_list)

    controller = ProductController()
    controller.product_repository = mock_db_session

    result = controller.list_products(None, None)

    assert len(result) == result_length
    assert all(result[i].id == product_model_list[i].id for i in range(result_length))
    assert all(result[i].name == product_model_list[i].name for i in range(result_length))
    assert all(result[i].description == product_model_list[i].description for i in range(result_length))
    assert all(result[i].price == product_model_list[i].price for i in range(result_length))
    assert all(result[i].inventory == product_model_list[i].inventory for i in range(result_length))
    assert all(result[i].category == product_model_list[i].category for i in range(result_length))
    assert all(result[i].created_at is not None for i in range(result_length))
    assert all(result[i].updated_at is not None for i in range(result_length))

# endregion

# region Create Product

def test_create_product_success(mock_db_session, helpers):

    product = helpers.generate_random_product()
    product_create_schema = ProductCreateSchemaBase(**product.dict())

    mock_db_session.create.return_value = copy.deepcopy(product)

    controller = ProductController()
    controller.product_repository = mock_db_session

    result = controller.create_product(product_create_schema)

    assert result.id == product.id
    assert result.name == product.name
    assert result.description == product.description
    assert result.price == product.price
    assert result.inventory == product.inventory
    assert result.category == product.category
    assert result.created_at == product.created_at
    assert result.updated_at == product.updated_at

def test_create_product_conflict(mock_db_session, helpers):
    product = helpers.generate_random_product()
    product_create_schema = ProductCreateSchemaBase(**product.dict())

    mock_db_session.create.side_effect = IntegrityError(
        "Product name conflict", "Product name conflict", "Product name conflict")

    controller = ProductController()
    controller.product_repository = mock_db_session

    with pytest.raises(SanicException) as exec:
        controller.create_product(product_create_schema)

    assert exec.value.status_code == 409
    assert exec.value.message == ERROR_409_MESSAGE

# endregion

# region Update Product

def test_update_product_success(mock_db_session, helpers):

    product = helpers.generate_random_product()

    product_updated = helpers.generate_random_product()
    product_updated.id = product.id

    values_to_update = ProductUpdateSchemaBase(**product_updated.dict())

    mock_db_session.find.return_value = copy.deepcopy(product)
    mock_db_session.update.return_value = copy.deepcopy(product_updated)

    controller = ProductController()
    controller.product_repository = mock_db_session

    result = controller.update_product(product.id, values_to_update)

    assert result.id == product_updated.id
    assert result.name == product_updated.name
    assert result.description == product_updated.description
    assert result.price == product_updated.price
    assert result.inventory == product_updated.inventory
    assert result.category == product_updated.category
    assert result.created_at == product_updated.created_at
    assert result.updated_at == product_updated.updated_at
    

def test_update_product_not_found(mock_db_session, helpers):

    mock_db_session.find.return_value = None

    controller = ProductController()
    controller.product_repository = mock_db_session

    with pytest.raises(SanicException) as exec:
        controller.update_product(9999, {})

    assert exec.value.status_code == 404
    assert exec.value.message == ERROR_404_MESSAGE


def test_update_product_conflict(mock_db_session, helpers):

    product = helpers.generate_random_product()

    product_updated = helpers.generate_random_product()
    product_updated.id = product.id

    values_to_update = ProductUpdateSchemaBase(**product_updated.dict())

    mock_db_session.find.return_value = copy.deepcopy(product)
    mock_db_session.update.side_effect = IntegrityError(
        "Product name conflict", "Product name conflict", "Product name conflict")

    controller = ProductController()
    controller.product_repository = mock_db_session

    with pytest.raises(SanicException) as exec:
        controller.update_product(product.id, values_to_update)

    assert exec.value.status_code == 409
    assert exec.value.message == ERROR_409_MESSAGE

# endregion

# region Delete Product

def test_delete_product_success(mock_db_session, helpers):

    product = helpers.generate_random_product()

    mock_db_session.find.return_value = product

    controller = ProductController()
    controller.product_repository = mock_db_session

    controller.delete_product(product.id)

def test_delete_product_not_found(mock_db_session):

    mock_db_session.find.return_value = None

    controller = ProductController()
    controller.product_repository = mock_db_session

    with pytest.raises(SanicException) as exec:
        controller.delete_product(9999)

    assert exec.value.status_code == 404
    assert exec.value.message == ERROR_404_MESSAGE

# endregion