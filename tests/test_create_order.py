import allure
from data.data import ExpectedResponses, StatusCodes, DataUser
from helpers.api_helpers import UserAPI, OrderAPI

class TestCreateOrder:
    @allure.title("Создание заказа авторизованным пользователем")
    def test_create_order_with_auth(self, create_user, delete_user):
        _, data, token = create_user()
        
        with allure.step("Авторизовать пользователя"):
            data_login = {"email": data["email"], "password": data["password"]}
            _, token = UserAPI.login_user(data_login)
        
        with allure.step("Создать заказ с валидными ингредиентами"):
            response_order = OrderAPI.create_order(DataUser.valid_ingredients, token)
            response_data = response_order.json()
        
        with allure.step("Проверить ответ сервера"):
            assert response_order.status_code == StatusCodes.ok
            assert isinstance(response_data.get('name'), str)
            assert isinstance(response_data.get('order'), dict)
            assert isinstance(response_data['order'].get('number'), int)
            assert response_data.get('success') is True
        delete_user(token)
    
    @allure.title("Создание заказа неавторизованным пользователем")
    def test_create_order_without_auth(self, create_user, delete_user):
        _, _, token = create_user()
        
        with allure.step("Создать заказ без авторизации"):
            response_order = OrderAPI.create_order(DataUser.valid_ingredients)
        
        with allure.step("Проверить ошибку авторизации"):
            assert response_order.status_code == StatusCodes.unauthorized
            response_data = response_order.json()
            assert response_data == ExpectedResponses.unauthorized_order
        
        delete_user(token)
    
    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self, create_user, delete_user):
        _, data, token = create_user()
        
        with allure.step("Авторизовать пользователя"): 
            data_login = {"email": data["email"], "password": data["password"]}
            _, token = UserAPI.login_user(data_login)
        
        with allure.step("Создать заказ без ингредиентов"):
            response_order = OrderAPI.create_order([], token)
            response_data = response_order.json()
        
        with allure.step("Проверить ошибку валидации"):
            assert response_order.status_code == StatusCodes.bad_request 
            assert response_data == ExpectedResponses.create_order_no_ingredients
        
        delete_user(token)

    @allure.title("Создание заказа с невалидным хешем ингредиентов")
    def test_create_order_invalid_ingredients_hash(self, create_user, delete_user):
        _, data, token = create_user()
        
        with allure.step("Авторизовать пользователя"): 
            data_login = {"email": data["email"], "password": data["password"]}
            _, token = UserAPI.login_user(data_login)
        
        with allure.step("Создать заказ с невалидными ингредиентами"):
            response_order = OrderAPI.create_order(DataUser.invalid_ingredients, token)
        
        with allure.step("Проверить ошибку сервера"):
            assert response_order.status_code == StatusCodes.internal_server_error
        
        delete_user(token)