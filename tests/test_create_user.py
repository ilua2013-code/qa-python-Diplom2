import allure
from data.data import ExpectedResponses, StatusCodes, DataUser
import pytest 
from generators.generator_data import CreateUser
from helpers.api_helpers import UserAPI
from helpers.data_helpers import modify_data

class TestCreateUser:
    @allure.title("Создание пользователя с валидными данными")
    @allure.description("Проверка успешного создания нового пользователя с корректными данными")
    def test_create_user(self, create_user, delete_user):
        with allure.step("Создать пользователя с валидными данными"):
            response, data, token = create_user()
            response_data = response.json()
        
        with allure.step("Проверить статус код ответа"):
            assert response.status_code == StatusCodes.ok, f"Ожидался статус {StatusCodes.ok}, получен {response.status_code}"
        
        with allure.step("Проверить структуру ответа"):
            assert response_data.get('success') is True, "Поле 'success' должно быть True"
            assert isinstance(response_data.get('user'), dict), "Поле 'user' должно быть словарем"
            assert isinstance(response_data.get('accessToken'), str), "Поле 'accessToken' должно быть строкой"
            assert isinstance(response_data.get('refreshToken'), str), "Поле 'refreshToken' должно быть строкой"
        
        with allure.step("Проверить формат токена"):
            assert response_data['accessToken'].startswith('Bearer '), "accessToken должен начинаться с 'Bearer '"
        delete_user(token)

    @allure.title("Создание пользователя который уже зарегистрирован")
    @allure.description("Проверка что нельзя создать пользователя с email который уже существует в системе")
    def test_create_user_already_exists(self, create_user, delete_user):
        _, data, token = create_user()
        with allure.step("Создать пользователя с данными которые уже есть в баз данных"):
            second_response = UserAPI.create_user_invalid(data)
        with allure.step("Проверить статус код ответа"):
            assert second_response.status_code == StatusCodes.forbidden, f"Ожидался статус {StatusCodes.forbidden}, \
            получен {second_response.status_code}"
            second_response_data = second_response.json()
            expected_response = ExpectedResponses.create_user_conflict
            assert second_response_data == expected_response, f"Ответ не совпадает с ожидаемым.\
            Получено: {second_response_data}, ожидалось: {expected_response}"
        delete_user(token)

    @allure.title("Создание пользователя с пустыми или отсутствующими полями")
    @allure.description("Проверка валидации при создании пользователя с пустыми или null значениями в обязательных полях")
    @pytest.mark.parametrize("field, value", DataUser.invalid_data_user)
    def test_create_user_invalid_data(self, field, value, create_user):
        with allure.step(f"Поле '{field}' со значением '{value}'"):
            data = CreateUser.generate_full_user()
            data = modify_data(data, field, value)
            response, _, _ = create_user(data)
        with allure.step("Проверить статус код ответа"):
            assert response.status_code == StatusCodes.forbidden, f"Ожидался статус {StatusCodes.forbidden}, \
            получен {response.status_code}"
        with allure.step("Проверить тело ответа"):
            second_response_data = response.json()
            expected_response = ExpectedResponses.create_user_missing_fields
            assert second_response_data == expected_response, f"Ответ не совпадает с ожидаемым.\
            Получено: {second_response_data}, ожидалось: {expected_response}"
        
    @allure.title("Создание пользователя без обязательных полей")
    @allure.description("Проверка что нельзя создать пользователя без указания всех обязательных полей")
    @pytest.mark.parametrize("data_user", DataUser.user_data_missing_fields)
    def test_create_user_invalid_data_not_field(self, data_user, create_user):
        with allure.step(f"Тестовые данные: {data_user}"):
            response, data_user, _ = create_user(data_user)
        with allure.step("Проверить статус код ответа"):
            assert response.status_code == StatusCodes.forbidden, f"Ожидался статус {StatusCodes.forbidden}, \
            получен {response.status_code}"
        with allure.step("Проверить тело ответа"):
            second_response_data = response.json()
            expected_response = ExpectedResponses.create_user_missing_fields
            assert second_response_data == expected_response, f"Ответ не совпадает с ожидаемым.\
            Получено: {second_response_data}, ожидалось: {expected_response}"
        