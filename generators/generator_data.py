from faker import Faker
class CreateUser:
    fake = Faker(locale = 'ru_RU')
    
    
    
    @classmethod
    def generation_user_email(cls):
        return cls.fake.email()
        
    @classmethod
    def generation_user_password(cls):
        return cls.fake.password()
    
    @classmethod
    def generation_user_name(cls):
        return cls.fake.first_name()
    
    
    @classmethod
    def generate_full_user(cls):
        """Генерация полного уникального курьера"""
        return {
            "email": cls.generation_user_email(),
            "password": cls.generation_user_password(),
            "name": cls.generation_user_name()
        }
    