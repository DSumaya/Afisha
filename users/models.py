from django.db import models
import random

class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.username

"""Модель для хранения кода подтверждения для пользователя"""
class ConfirmUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1, related_name="confirm_code")
    code = models.CharField(max_length=6, null=True)


    """Генерация случайного 6-значного кода при создании"""
    def save(self, *args, **kwargs):
        if not self.code:
            self.code = "".join([str(random.randint(0, 9)) for _ in range(6)])
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Code for {self.user}: {self.code}"