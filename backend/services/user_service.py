from django.contrib.auth.base_user import BaseUserManager
from repositories.user_repository import TemporaryPasswordRepository
from repositories.user_repository import UserRepository
from user.tasks import send_email_task


class UserService:
    def __init__(self, user_repository: UserRepository, temp_password_repository: TemporaryPasswordRepository):
        self.user_repository = user_repository
        self.temp_password_repository = temp_password_repository

    def create_temp_password(self):
        password = BaseUserManager().make_random_password()
        return password

    def send_password_to_user(self, email, password):
        send_email_task.delay(email, password)

    def create_user(self, data):
        user = self.user_repository.create_user(
            email=data["email"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            phone_number=data["phone_number"],
        )
        return user

    def login_user(self, email):
        user = self.user_repository.get_user(email)
        if user:
            temp_password = self.create_temp_password()
            print(temp_password)
            self.temp_password_repository.create_temporary_password(user, temp_password)
            self.send_password_to_user(user.email, temp_password)
            return user
        return None

    def get_or_create_user(self, data):
        email = data["email"]
        user = self.user_repository.get_user(email)
        if not user:
            user = self.create_user(data)
        return user

    def check_user_data(self, user, data):
        fields_to_check = ["first_name", "last_name", "phone_number"]
        if any(getattr(user, field) != data.get(field) for field in fields_to_check):
            self.user_repository.update_user(user, data)

    def authenticate_user(self, email, password):
        user = self.user_repository.get_user(email)
        if not user:
            return None

        temp_password_record = self.temp_password_repository.get_valid_temporary_password(user)
        if temp_password_record and password == temp_password_record.code:
            return user
        return None

    def is_email_free(self, email):
        return self.user_repository.is_email_free(email)

    def is_phone_free(self, phone):
        return self.user_repository.is_phone_free(phone)
