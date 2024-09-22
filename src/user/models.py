from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from ..abstract.models import AbstractModel, AbstractManager


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return "user_{0}/{1}".format(instance.public_id, filename)


class UserManager(BaseUserManager, AbstractManager):
    def create_google_user(self,email,password=None,**kwargs):
        if email is None:
            raise TypeError("Users must have an email.")
        if password is None:
            raise TypeError("User must have an email.")
        user = self.model(
             email=self.normalize_email(email), **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        user.save(using=self._db)
        return user
    def create_user(self, email, password=None, **kwargs):
        """Create and return a `User` with an email, phone number, username and password."""
        if email is None:
            raise TypeError("Users must have an email.")
        if password is None:
            raise TypeError("User must have an email.")

        user = self.model(
             email=self.normalize_email(email), **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **kwargs):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError("Superusers must have a password.")
        if email is None:
            raise TypeError("Superusers must have an email.")

        user = self.create_user( email, password, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractModel, AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    avatar = models.ImageField(null=True, blank=True, upload_to=user_directory_path)

    
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"

    objects = UserManager()

    def __str__(self):
        return f"{self.email}"

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"
