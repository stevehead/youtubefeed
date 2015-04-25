from django.db import models


class BaseModel(models.Model):
    is_active = models.BooleanField(default=True)
    record_created_at = models.DateTimeField('record creation time', auto_now_add=True)
    record_updated_at = models.DateTimeField('record update time', auto_now=True)

    def __init__(self, *args, **kwargs):
        super(BaseModel, self).__init__(*args, **kwargs)
        self._cache_info = dict()

    def save(self, *args, **kwargs):
        super(BaseModel, self).save(*args, **kwargs)
        self._cache_info = dict()

    class Meta:
        abstract = True