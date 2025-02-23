from django.db import models

class ConfirmUser(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name="confirm_code")
    code = models.CharField(max_length=6, null=False)

    def __str__(self) -> str:
        return f'{self.code} - {self.user.username}'


