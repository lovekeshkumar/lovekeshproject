from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Usermodel(User):
    class Meta:
        db_table = "user"
        verbose_name = "user"
        verbose_name_plural = "user"