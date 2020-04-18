from django.db import models


class Publication(models.Model):
    name = models.CharField(max_length=120)
    date = models.DateTimeField()
    text = models.TextField()
