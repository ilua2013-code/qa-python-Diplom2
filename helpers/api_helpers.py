import requests
from data.url import Url

class UserAPI:
    
    @staticmethod
    def login_user(data):
        """Авторизация пользователя"""
        response = requests.post(f'{Url.autoriza_user}', json=data) 
        token = response.json().get("accessToken")
        return response, token
    
    @staticmethod
    def create_user_invalid(invalid_data):
        """Создание пользователя с невалидными данными"""
        response = requests.post(f'{Url.create_user}', json=invalid_data)
        return response

class OrderAPI:
    
    @staticmethod
    def create_order(ingredients, token=None):
        """Создание заказа"""
        headers = {}
        if token is not None:
            headers['Authorization'] = token 
        data = {"ingredients": ingredients}
        response = requests.post(f'{Url.create_order}', json=data, headers=headers)
        return response