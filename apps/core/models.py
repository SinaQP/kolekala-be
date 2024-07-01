from django.db import models
from django.utils.text import slugify


class Model(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

class Setting(Model):
    language = models.CharField(max_length=4, choices=[('fa', 'Persian'), ('en', 'English')], default='en')

    @classmethod
    def get_by_primary_key(cls, primary_key):
        try:
            return cls.objects.get(pk=primary_key)
        except cls.DoesNotExist:
            return None

