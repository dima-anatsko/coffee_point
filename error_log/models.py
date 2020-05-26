from django.contrib.postgres.fields import JSONField
from django.db import models


class RequestError(models.Model):
    exception_name = models.CharField(max_length=50)
    exception_value = models.CharField(max_length=250)
    exception_tb = models.TextField()
    request_method = models.CharField(max_length=10)
    path = models.CharField(max_length=500)
    query = JSONField()
    data = JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at', )

    def __str__(self):
        return f'{self.exception_name}: {self.exception_value}'
