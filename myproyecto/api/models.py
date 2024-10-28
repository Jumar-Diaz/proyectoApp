from django.db import models

# Create your models here.
from django.db import models

class Recomendacion(models.Model):
    cluster = models.IntegerField()
    recomendaciones = models.TextField()
    images = models.TextField();
    description = models.TextField()

class Calificacion(models.Model):
    cluster = models.IntegerField()
    calification = models.IntegerField()


class CalificacionImage(models.Model):
    image_calification = models.IntegerField()
    image_name = models.CharField(max_length=255)