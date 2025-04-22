from django.db import models


class TimeModelMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    @property
    def class_name(self):
        return self.__class__.__name__

    class Meta:
        abstract = True
