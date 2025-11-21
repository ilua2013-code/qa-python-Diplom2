import pytest
from helpers.api_helpers import UserAPI


@pytest.fixture(scope="function")
def create_and_delete_user():
    """Фикстура создает пользователя и удаляет его после теста"""
    response, token, data = UserAPI.create_user()
    
    yield response, data
    
    UserAPI.delete_user(token)

