from django.contrib.auth.models import User
from django.db import models


class Vacancy(models.Model):
    description = models.CharField(max_length=1024)
    author = models.ForeignKey(
        User, related_name="vacancy",
        on_delete=models.CASCADE)
