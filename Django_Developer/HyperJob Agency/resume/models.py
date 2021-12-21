from django.contrib.auth.models import User
from django.db import models
from vacancy.models import Vacancy


# Create your models here.
class Resume(models.Model):
    description = models.CharField(max_length=1024)
    author = models.ForeignKey(
        User, related_name="resume",
        on_delete=models.CASCADE)

    vacancy = models.ForeignKey(
        Vacancy, related_name="resume",
        on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'resume_resume'
