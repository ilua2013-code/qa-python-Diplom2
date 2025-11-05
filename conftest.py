import requests
import pytest
from data.url import Url
from generators.generator_data import CreateUser



@pytest.fixture(scope="function")
def create_user():
    """Фикстура для создания пользователя"""
    def _create_user(custom_data=None):
        data = custom_data if custom_data else CreateUser.generate_full_user()
        response = requests.post(f'{Url.create_user}', json=data) 
        token = response.json().get("accessToken")
        return response, data, token
    
    return _create_user
@pytest.fixture(scope="function")
def delete_user():
    """Фикстура для удаления пользователя"""
    def _delete_user(auth_token):
        headers = {"Authorization": auth_token}
        response = requests.delete(f'{Url.delete_user}', headers=headers)
        return response
    return _delete_user

