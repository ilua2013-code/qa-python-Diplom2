import requests
from data.url import Url
from generators.generator_data import CreateUser
class UserAPI:
    
    
    @staticmethod
    def create_user():
        """Создание пользователя с валидными данными"""
        data = CreateUser.generate_full_user()
        response = requests.post(f'{Url.create_user}', json=data)
        token = response.json().get("accessToken")
        return response, token, data
    
    @staticmethod
    def login_user(data):
        """Авторизация пользователя"""
        response = requests.post(f'{Url.autoriza_user}', json=data) 
        token = response.json().get("accessToken")
        return response, token

    @staticmethod
    def delete_user(token):
        """Удаление пользователя"""
        headers = {"Authorization": token}
        response = requests.delete(f'{Url.delete_user}', headers=headers)
        return response

    @staticmethod
    def create_user_with_data(custom_data):
        """Создание пользователя с переданными данными"""
        response = requests.post(f'{Url.create_user}', json=custom_data)
        token = response.json().get("accessToken")  
        return response, token, custom_data

class OrderAPI:
    
    @staticmethod
    def create_order_with_auth(ingredients, token):
        """Создание заказа с авторизацией"""
        headers = {'Authorization': token}
        data = {"ingredients": ingredients}
        response = requests.post(f'{Url.create_order}', json=data, headers=headers)
        return response

    @staticmethod
    def create_order_without_auth(ingredients):
        """Создание заказа без авторизации"""
        data = {"ingredients": ingredients}
        response = requests.post(f'{Url.create_order}', json=data)
        return response