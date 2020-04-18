from django.db import models


class Message(models.Model):
    name = models.CharField(max_length=120)
    text = models.TextField()


class Publication(models.Model):
    name = models.CharField(max_length=120)
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
