from django.db import models


class BaseModel(models.Model):
    is_active = models.BooleanField(default=True)
    record_created_at = models.DateTimeField('record creation time', auto_now_add=True)
    record_updated_at = models.DateTimeField('record update time', auto_now=True)

    class Meta:
        abstract = True