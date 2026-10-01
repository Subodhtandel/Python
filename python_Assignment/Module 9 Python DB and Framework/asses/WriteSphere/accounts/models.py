from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "admin", "Administrator"
        AUTHOR = "author", "Author"
        READER = "reader", "Reader"

    email = models.EmailField("email address", unique=True, blank=True, null=True)
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.READER,
    )
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    bio = models.CharField(max_length=500, blank=True)

    class Meta:
        ordering = ["username"]

    def can_publish_posts(self) -> bool:
        return self.role in (
            User.Role.ADMIN,
            User.Role.AUTHOR,
        ) or self.is_superuser

    def __str__(self) -> str:
        return self.username
