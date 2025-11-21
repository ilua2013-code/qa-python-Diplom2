import allure
from data.data import ExpectedResponses, StatusCodes, DataUser
from helpers.api_helpers import UserAPI, OrderAPI

class TestCreateOrder:
    @allure.title("Создание заказа авторизованным пользователем")
    def test_create_order_with_auth(self, create_and_delete_user):
        data = create_and_delete_user[1]
        
        with allure.step("Авторизовать пользователя"):
            data_login = {"email": data["email"], "password": data["password"]}
            token = UserAPI.login_user(data_login)[1]
        
        with allure.step("Создать заказ с валидными ингредиентами"):
            response_order = OrderAPI.create_order_with_auth(DataUser.valid_ingredients, token)
            
        with allure.step("Проверить ответ сервера"):
            response_data = response_order.json()
            assert response_order.status_code == StatusCodes.ok
            assert isinstance(response_data.get('name'), str)
            assert isinstance(response_data.get('order'), dict)
            assert isinstance(response_data['order'].get('number'), int)
            assert response_data.get('success') is True
        
    
    @allure.title("Создание заказа неавторизованным пользователем")
    def test_create_order_without_auth(self):
        
        with allure.step("Создать заказ без авторизации"):
            response_order = OrderAPI.create_order_without_auth(DataUser.valid_ingredients)
            
        with allure.step("Проверить ответ сервера"):
            assert response_order.status_code == StatusCodes.unauthorized
            assert response_order.json() == ExpectedResponses.unauthorized_order
        
        
    
    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self, create_and_delete_user):
        data = create_and_delete_user[1]
        
        with allure.step("Авторизовать пользователя"): 
            data_login = {"email": data["email"], "password": data["password"]}
            token = UserAPI.login_user(data_login)[1]
        
        with allure.step("Создать заказ без ингредиентов"):
            response_order = OrderAPI.create_order_with_auth([], token)
            
        
        with allure.step("Проверить ответ сервера"):
            assert response_order.status_code == StatusCodes.bad_request 
            assert response_order.json() == ExpectedResponses.create_order_no_ingredients
        

    @allure.title("Создание заказа с невалидным хешем ингредиентов")
    def test_create_order_invalid_ingredients_hash(self, create_and_delete_user):
        data = create_and_delete_user[1]
        
        with allure.step("Авторизовать пользователя"): 
            data_login = {"email": data["email"], "password": data["password"]}
            token = UserAPI.login_user(data_login)[1]
        
        with allure.step("Создать заказ с невалидными ингредиентами"):
            response_order = OrderAPI.create_order_with_auth(DataUser.invalid_ingredients, token)
        
        with allure.step("Проверить ответ сервера"):
            assert response_order.status_code == StatusCodes.internal_server_error
        
        