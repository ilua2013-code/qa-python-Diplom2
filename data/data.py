from generators.generator_data import CreateUser

class ExpectedResponses:
    # Создание пользователя
    create_user_success = {
        "success": True,
        "user": {
            "email": "user@example.com",
            "name": "Username"
        },
        "accessToken": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "refreshToken": "abc123def456ghi789jkl012mno345pqr678stu901vwx234yz"
        }
    
    # Ошибки создания пользователя
    create_user_conflict = {
        "success": False,
        "message": "User already exists"
    }
    # Ошибки если нет одного из полей
    create_user_missing_fields = {
        "success": False,
        "message": "Email, password and name are required fields"
    }
    unauthorized_login = {
        "success": False,
        "message": "email or password are incorrect"
    }
    # Создание заказа
    create_order_success = {
        "name": "Краторный метеоритный бургер",
        "order": {
            "number": 6257
        },
        "success": True
    }
    # Ошибка при отсутствии ингредиентов 
    create_order_no_ingredients = {
        "success": False,
        "message": "Ingredient ids must be provided"
    }

    unauthorized_order = {
    "success": False,
    "message": "You should be authorised"
}
class StatusCodes:
    ok = 200
    created = 201
    bad_request = 400
    unauthorized = 401
    forbidden = 403
    not_found = 404
    conflict = 409
    internal_server_error = 500
    
class DataUser:
    user_data_missing_fields = [
    {"name": CreateUser.generation_user_name(), "password": CreateUser.generation_user_password()},
    {"email": CreateUser.generation_user_email(), "password": CreateUser.generation_user_password()},
    {"email": CreateUser.generation_user_email(), "name": CreateUser.generation_user_name()},
    {"email": CreateUser.generation_user_email()},
    {"name": CreateUser.generation_user_name()},
    {"password": CreateUser.generation_user_password()},
    {}
]
    valid_ingredients = ["61c0c5a71d1f82001bdaaa6f", "61c0c5a71d1f82001bdaaa6d"]
    invalid_ingredients = ["i48484949939393"]         
    invalid_data_user = ("email", None), ("password", None), ("name", None), ("email", ""), ("password", ""), ("name", "")
    