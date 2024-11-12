import pytest
import math
import random
import string
from datetime import datetime
from unittest.mock import Mock

from models.product_model import ProductModel


class Helpers:

    def _random_str(self, min: int, max: int) -> str:
        rand_alphabet = string.ascii_letters + string.digits
        return ''.join([random.choice(rand_alphabet) for i in range(random.randint(min, max))])

    def _random_float(self, min: int, max: int) -> float:
        price_base = random.randint(min, max)
        price_weight = random.random()
        price = math.floor(price_base * price_weight * 100)/100
        return price
    
    def generate_random_product(self) -> ProductModel:

        return ProductModel(
            id=random.randint(1, 9999),
            name=self._random_str(5, 30),
            description=self._random_str(30, 200),
            price=self._random_float(10, 100),
            inventory=random.randint(1, 300),
            category=self._random_str(5, 30),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
    

@pytest.fixture
def mock_db_session():
    return Mock()

@pytest.fixture
def helpers():
    return Helpers()
    