from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models

phone_regex = RegexValidator(regex='^0[0-9]{2,}[0-9]{7,}$', message='phone number is invalid')


class Entry(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(validators=[phone_regex], max_length=11)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return f'{self.name} {self.last_name}'
