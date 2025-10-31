import allure
from data.data import ExpectedResponses, StatusCodes, DataUser


class TestCreateOrder:
    @allure.title("Создание заказа авторизованным пользователем")
    @allure.description("Проверка успешного создания заказа с валидными ингредиентами для авторизованного пользователя")
    def test_create_order_with_auth(self, create_user, login_user, delete_user, do_order):
        _, data, token = create_user()
        data_login = {"email": data["email"], "password": data["password"]}
        _, token = login_user(data_login) 
        response_order = do_order(DataUser.valid_ingredients, token)
        response_data = response_order.json()
        assert response_order.status_code == StatusCodes.ok
        assert isinstance(response_data.get('name'), str)
        assert isinstance(response_data.get('order'), dict)
        assert isinstance(response_data['order'].get('number'), int)
        assert response_data.get('success') is True
        delete_user(token)
    
    @allure.title("Создание заказа неавторизованным пользователем")
    @allure.description("Проверка что неавторизованный пользователь не может создать заказ и получает ошибку 401")
    def test_create_order_without_auth(self, create_user, delete_user, do_order):
        response, data, token = create_user()
        response_order = do_order(DataUser.valid_ingredients)
        assert response_order.status_code == StatusCodes.unauthorized, f"Ожидался статус {StatusCodes.unauthorized}, получен {response_order.status_code}"
        response_data = response_order.json()
        assert response_data == ExpectedResponses.unauthorized_order, f"Ответ не совпадает с ожидаемым. Получено: {response_data}, ожидалось: {ExpectedResponses.unauthorized_order}"
        delete_user(token)
    
    @allure.title("Создание заказа без ингредиентов")
    @allure.description("Проверка что нельзя создать заказ без указания ингредиентов")
    def test_create_order_without_ingredients(self, create_user, login_user, delete_user, do_order):
        _, data, token = create_user()
        data_login = {"email": data["email"], "password": data["password"]}
        _, token = login_user(data_login) 
        response_order = do_order([], token)
        response_data = response_order.json()
        assert response_order.status_code == StatusCodes.bad_request 
        assert response_data == ExpectedResponses.create_order_no_ingredients, f"Ответ не совпадает с ожидаемым. Получено: {response_data}, ожидалось: {ExpectedResponses.create_order_no_ingredients}"
        delete_user(token)

    @allure.title("Создание заказа с невалидным хешем ингредиентов")
    @allure.description("Проверка обработки ошибки при создании заказа с несуществующими ингредиентами")
    def test_create_order_invalid_ingredients_hash(self, create_user, login_user, delete_user, do_order):
        _, data, token = create_user()
        data_login = {"email": data["email"], "password": data["password"]}
        _, token = login_user(data_login) 
        response_order = do_order(DataUser.invalid_ingredients, token) 
        assert response_order.status_code == StatusCodes.internal_server_error 
        print(f"Response text: {response_order.text}")
        delete_user(token)