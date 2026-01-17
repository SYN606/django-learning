from django.db import models

class Blog(models.Model):
    title = models.CharField(max_length=250, blank=False, null=False)
    contents = models.TextField()
    