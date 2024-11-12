import copy
from unittest.mock import MagicMock
from sqlalchemy import select, func
from models.product_model import ProductModel
from repositories.product_repository import ProductRepository


def test_list_product_success(mock_db_session, helpers):

    return_size = 10
    product_model_list = [helpers.generate_random_product() for _ in range(return_size)]

    mock_scalars = MagicMock()
    mock_scalars.all.return_value = copy.deepcopy(product_model_list)

    mock_execute = MagicMock()
    mock_execute.scalars.return_value = mock_scalars

    mock_db_session.execute.return_value = mock_execute

    repository = ProductRepository()
    repository.session = mock_db_session

    result = repository.list(None, None)

    assert len(result) == return_size
    assert all(result[i].id == product_model_list[i].id for i in range(return_size))
    assert all(result[i].name == product_model_list[i].name for i in range(return_size))
    assert all(result[i].description == product_model_list[i].description for i in range(return_size))
    assert all(result[i].price == product_model_list[i].price for i in range(return_size))
    assert all(result[i].inventory == product_model_list[i].inventory for i in range(return_size))
    assert all(result[i].category == product_model_list[i].category for i in range(return_size))
    assert all(result[i].created_at is not None for i in range(return_size))
    assert all(result[i].updated_at is not None for i in range(return_size))


def test_list_with_params_product_success(mock_db_session, helpers):

    return_size = 10
    product_model_list = [helpers.generate_random_product() for _ in range(return_size)]

    filters = {
        "category": "Eletrodomesticos",
        "price": 300
    }

    sort_by = "id"

    expected_query = select(ProductModel).filter(
        func.lower(ProductModel.category).contains(filters["category"].lower())
    ).filter(
        ProductModel.price == filters["price"]
    ).order_by(
        ProductModel.id
    )

    mock_scalars = MagicMock()
    mock_scalars.all.return_value = copy.deepcopy(product_model_list)

    mock_execute = MagicMock()
    mock_execute.scalars.return_value = mock_scalars

    mock_db_session.execute.return_value = mock_execute

    repository = ProductRepository()
    repository.session = mock_db_session

    result = repository.list(filters, sort_by)

    called_query = mock_db_session.execute.call_args[0][0]

    assert len(result) == return_size
    assert all(result[i].id == product_model_list[i].id for i in range(return_size))
    assert all(result[i].name == product_model_list[i].name for i in range(return_size))
    assert all(result[i].description == product_model_list[i].description for i in range(return_size))
    assert all(result[i].price == product_model_list[i].price for i in range(return_size))
    assert all(result[i].inventory == product_model_list[i].inventory for i in range(return_size))
    assert all(result[i].category == product_model_list[i].category for i in range(return_size))
    assert all(result[i].created_at is not None for i in range(return_size))
    assert all(result[i].updated_at is not None for i in range(return_size))
    assert str(called_query) == str(expected_query)

def test_find_product_success(mock_db_session, helpers):

    product = helpers.generate_random_product()

    mock_unique = MagicMock()
    mock_unique.one_or_none.return_value = copy.deepcopy(product)

    mock_scalars = MagicMock()
    mock_scalars.unique.return_value = mock_unique

    mock_execute = MagicMock()
    mock_execute.scalars.return_value = mock_scalars

    mock_db_session.execute.return_value = mock_execute

    repository = ProductRepository()
    repository.session = mock_db_session

    result = repository.find(product.id)

    assert product.id == result.id
    assert product.name == result.name
    assert product.description == result.description
    assert product.price == result.price
    assert product.inventory == result.inventory
    assert product.category == result.category
    assert product.created_at == result.created_at
    assert product.updated_at == result.updated_at
    

def test_create_product_success(mock_db_session, helpers):

    repository = ProductRepository()
    repository.session = mock_db_session

    product = helpers.generate_random_product()

    created_product = repository.create(copy.deepcopy(product))

    assert created_product.id == product.id
    assert created_product.name == product.name
    assert created_product.description == product.description
    assert created_product.price == product.price
    assert created_product.inventory == product.inventory
    assert created_product.category == product.category
    assert created_product.created_at != product.created_at
    assert created_product.updated_at != product.updated_at

    mock_db_session.add.assert_called()
    mock_db_session.commit.assert_called()


def test_update_product_success(mock_db_session, helpers):

    repository = ProductRepository()
    repository.session = mock_db_session

    product = helpers.generate_random_product()

    values_to_update = helpers.generate_random_product()

    updated_product = repository.update(copy.deepcopy(product), values_to_update)

    assert updated_product.id != values_to_update.id
    assert updated_product.name == values_to_update.name
    assert updated_product.description == values_to_update.description
    assert updated_product.price == values_to_update.price
    assert updated_product.inventory == values_to_update.inventory
    assert updated_product.category == values_to_update.category
    assert updated_product.created_at != values_to_update.created_at
    assert updated_product.updated_at != values_to_update.updated_at
    assert updated_product.created_at < updated_product.updated_at

    mock_db_session.commit.assert_called()
    mock_db_session.refresh.assert_called()


def test_delete_product_success(mock_db_session, helpers):

    repository = ProductRepository()
    repository.session = mock_db_session

    repository.delete(helpers.generate_random_product())

    mock_db_session.delete.assert_called()
    mock_db_session.commit.assert_called()

