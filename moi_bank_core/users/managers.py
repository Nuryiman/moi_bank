from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    """Кастомный менеджер"""

    def create_user(self, phone_number, password, **extra_fields):
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True
        extra_fields['is_active'] = True
        return self.create_user(phone_number, password, **extra_fields)
