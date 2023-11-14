from django.contrib.auth.models import AbstractUser, Permission, Group, UserManager
from django.db import models


class User(AbstractUser):
    """
    Default User model provided by Django.

    This model includes fields for storing email, first name, last name, etc.
    It inherits from AbstractUser, which includes the common fields and methods for a user.
    """
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_dev = models.BooleanField(default=False)
    joined_date = models.DateField(null=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    # Add related_name to avoid clashes with auth.User
    groups = models.ManyToManyField(
        "auth.Group",
        verbose_name="groups",
        blank=True,
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
        related_name="maasapp_user_set",
    )

    user_permissions = models.ManyToManyField(
        "auth.Permission",
        verbose_name="user permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        related_name="maasapp_user_set",
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        """Method for returning the readable representation of an object, in this case the email"""
        return self.email

