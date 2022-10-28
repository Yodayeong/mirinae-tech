from django.db import models

class Emotion(models.Model):
    content = models.TextField()
