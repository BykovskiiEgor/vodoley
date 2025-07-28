from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, phone_number, password=None, **extra_fields):
        """Create and save a user with the given email and optional password."""
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            **extra_fields,
        )
        if not password:
            password = self.make_random_password()
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, phone_number, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and optional password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)

        user = self.model(
            email=email,
            first_name=first_name,
            phone_number=phone_number,
            **extra_fields,
        )

        if password:
            user.set_password(password)
        else:
            raise ValueError(_("Superuser must have a password."))

        user.save(using=self._db)
        return user
