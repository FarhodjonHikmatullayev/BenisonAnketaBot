from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=221, null=True, blank=True)
    last_name = models.CharField(max_length=221, null=True, blank=True)
    username = models.CharField(max_length=221, null=True, blank=True)
    phone = models.CharField(max_length=13, null=True, blank=True)
    telegram_id = models.BigIntegerField(unique=True)

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Foydalanuvchilar'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
