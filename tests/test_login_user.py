import allure
from data.data import ExpectedResponses, StatusCodes


class TestLoginUser:
    
    @allure.title("Успешная авторизация пользователя")
    @allure.description("Проверка успешного входа в систему с валидными учетными данными")
    def test_login_user(self, create_user, login_user, delete_user):
        _, data, token = create_user()
        login_data = {"email": data["email"], "password": data["password"]}
        response_login, _ = login_user(login_data) 
        response_data = response_login.json()
        
        assert response_login.status_code == StatusCodes.ok, f"Ожидался статус {StatusCodes.ok}, получен {response_login.status_code}"
        
        # Проверка структуры ответа
        assert response_data.get('success') is True, "Поле 'success' должно быть True"
        assert response_data['accessToken'].startswith('Bearer '), "accessToken должен начинаться с 'Bearer '"
        assert isinstance(response_data.get('accessToken'), str), "Поле 'accessToken' должно быть строкой"
        assert isinstance(response_data.get('refreshToken'), str), "Поле 'refreshToken' должно быть строкой"
        assert isinstance(response_data.get('user'), dict), "Поле 'user' должно быть словарем"
        
        assert response_data['user']['email'] == data['email'], f"Email не совпадает. Ожидался: {data['email']}, получен: {response_data['user']['email']}"
        assert response_data['user']['name'] == data['name'], f"Name не совпадает. Ожидался: {data['name']}, получен: {response_data['user']['name']}"
        
        delete_user(token)

    
    @allure.title("Авторизация с неверным паролем")
    @allure.description("Проверка обработки ошибки при вводе неправильного пароля")
    def test_login_invalid_password(self, create_user, login_user, modify_data, delete_user):
        _, data, token = create_user()
        invalid_login_data = modify_data(
            {"email": data["email"], "password": data["password"]}, 
            "password", "wrong_password"
        )
        response, _ = login_user(invalid_login_data)
        response_data = response.json()
        
        assert response.status_code == StatusCodes.unauthorized, "Должна быть ошибка при неверном пароле"
        assert response_data == ExpectedResponses.unauthorized_login, (
            f"Ответ не совпадает с ожидаемым. Получено: {response_data}, ожидалось: {ExpectedResponses.unauthorized_login}"
        )
        
        delete_user(token)

    @allure.title("Авторизация с неверным email")
    @allure.description("Проверка обработки ошибки при вводе неправильного email")
    def test_login_invalid_email(self, create_user, login_user, modify_data, delete_user):
        _, data, token = create_user()
        invalid_login_data = modify_data(
            {"email": data["email"], "password": data["password"]}, 
            "email", "wrong@email.com"
        )
        response, _ = login_user(invalid_login_data)
        response_data = response.json()
        
        assert response.status_code == StatusCodes.unauthorized, "Должна быть ошибка при неверном email"
        assert response_data == ExpectedResponses.unauthorized_login, (
            f"Ответ не совпадает с ожидаемым. Получено: {response_data}, ожидалось: {ExpectedResponses.unauthorized_login}"
        )
        
        delete_user(token)
    
    @allure.title("Авторизация с неверным email и паролем")
    @allure.description("Проверка обработки ошибки при вводе неправильного email и пароля")
    def test_login_invalid_both(self, login_user, delete_user, create_user):
        _, data, token = create_user()
        invalid_login_data = {"email": "wrong@email.com", "password": "wrong_password"}
        response, _ = login_user(invalid_login_data)
        response_data = response.json()
        
        assert response.status_code == StatusCodes.unauthorized, "Должна быть ошибка при неверных данных"
        assert response_data == ExpectedResponses.unauthorized_login, (
            f"Ответ не совпадает с ожидаемым. Получено: {response_data}, ожидалось: {ExpectedResponses.unauthorized_login}"
        )
        
        delete_user(token)