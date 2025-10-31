import allure
import requests
import pytest
from data.url import Url
from generators.generator_data import CreateUser
from data.data import StatusCodes


@pytest.fixture(scope="function")
def create_user():
    """Фикстура для создания пользователя"""
    def _create_user(custom_data=None):
        with allure.step("Создаем пользователя"):
            # Используем переданные данные или генерируем новые
            data = custom_data if custom_data else CreateUser.generate_full_user()
            response = requests.post(f'{Url.create_user}', json=data) 
            token = response.json().get("accessToken") if response.status_code == StatusCodes.ok else None
            
            if response.status_code == StatusCodes.ok:
                print(f"Пользователь успешно создан")
            else:
                print(f"Не удалось создать пользователя: {response.status_code}")
                
            return response, data, token
    
    return _create_user


@pytest.fixture(scope="function")
def login_user():
    """Фикстура для авторизации пользователя"""
    def _login_user(data):
        with allure.step("Авторизация пользователя"):
            response = requests.post(f'{Url.autoriza_user}', json=data) 
            token = response.json().get("accessToken")
            if response.status_code == StatusCodes.ok:
                print(f"Пользователь успешно авторизован")
            else:
                print(f"Не удалось авторизоваться: {response.status_code}")
                
            return response, token
    
    return _login_user

@pytest.fixture(scope="function")
def create_user_invalid():
    """Фикстура для создания пользователя с невалидными данными"""
    def _create_user_invalid(invalid_data):
        with allure.step("Создаем пользователя с невалидными данными"):
            response = requests.post(f'{Url.create_user}', json=invalid_data)
            return response 
    
    return _create_user_invalid

@pytest.fixture(scope="function")
def delete_user():
    """Фикстура для удаления пользователя"""
    def _delete_user(auth_token):
        with allure.step("Удаляем пользователя"):
            headers = {"Authorization": auth_token}
            response = requests.delete(f'{Url.delete_user}', headers=headers)
            
            if response.status_code == StatusCodes.ok:
                print(f"Пользователь успешно удален")
            else:
                print(f"Не удалось удалить пользователя: {response.status_code}")
            return response
    
    return _delete_user

@pytest.fixture
def modify_data():
    """Фикстура для изменения полей в данных"""
    def _modify_data(original_data, key, values):
        modified_data = original_data.copy() 
        modified_data[key] = values
        return modified_data
    
    return _modify_data

@pytest.fixture
def do_order():
    """Фикстура для создания заказа"""
    def _do_order(ingredients, token = None):
        headers = {}
        if token is not None:
            headers['Authorization'] = token 
        data = {"ingredients": ingredients}
        response = requests.post(f'{Url.create_order}', json=data,  headers =  headers)
        return response
    return _do_order