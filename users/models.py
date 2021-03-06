import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):

    user_uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    class Meta:
        db_table = 'auth_user'
