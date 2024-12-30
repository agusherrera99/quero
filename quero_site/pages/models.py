from django.db import models


class User(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=80)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)

    def __str__(self):
        return self.email