from django.db import models


class Students(models.Model):
    name = models.CharField(max_length=50)
    id_number = models.CharField(max_length=10)
    role = models.CharField(max_length=50)
    about = models.TextField()
