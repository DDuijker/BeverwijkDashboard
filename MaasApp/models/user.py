"""In this file we will create a user model"""
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
# AbstractUser is the foundation for creating a model, with authentication
# BasUserManager to provide helper methods for creating and managing user accounts
# PermissionMixin adds fields and methods related to user permissions
# User model is defined in settings.py because it is a custom user


class UserManager(BaseUserManager):
    """
    Custom user manager for the CustomUser model.

    This manager provides methods for creating and managing user accounts.
    It allows for the creation of regular users and superusers with appropriate privileges.
    The manager handles user authentication and user data validation.
    """
    def create_user(self, email, password=None, **extra_fields):
        """This method creates a normal user"""
        if not email:
            raise ValueError("Email is vereist!")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """This method creates a superuser, with more functionality and permissions"""
        extra_fields.setdefault('is_dev', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_dev') is not True:
            raise ValueError("Superuser must have is_dev=True")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
      Custom user model for the application.

      This model represents the user accounts in the application.
      It includes fields for storing email, first name, and last name.
      CustomUser also manages user authentication and authorization.
      """
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_dev = models.BooleanField(default=False)
    joined_date = models.DateField(null=True)
    is_staff = models.BooleanField(default=False)

    # Makes it easier to manage user objects
    objects = UserManager()

    # We use the email as our identifier instead of an username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        """Method for returning the readable representation of an object, in this case the email"""
        return self.email



