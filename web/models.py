from django.db import models


class Message(models.Model):
    name = models.CharField(max_length=120)
    text = models.TextField()


class Publication(models.Model):
    name = models.CharField(max_length=120)
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    likes = models.IntegerField(default=0)


class Comment(models.Model):
    publication = models.ForeignKey(Publication,
        on_delete=models.PROTECT, related_name='comments')
    name = models.CharField(max_length=120)
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    likes = models.IntegerField(default=0)
