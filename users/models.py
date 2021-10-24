from django.db   import models
from core.models import TimeStampModel

class User(TimeStampModel):
    email        = models.EmailField(max_length = 100, unique = True)
    password     = models.CharField(max_length = 200)
    name         = models.CharField(max_length = 50)
    phone_number = models.CharField(max_length = 20, null = True)

    class Meta:
        db_table = 'users'
