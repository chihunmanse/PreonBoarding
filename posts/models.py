from django.db   import models
from core.models import TimeStampModel

class Post(TimeStampModel):
    user       = models.ForeignKey('users.User', on_delete = models.CASCADE)
    title      = models.CharField(max_length = 50)
    content    = models.TextField()

    class Meta:
        db_table = 'posts'

