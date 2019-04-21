from django.db import models

# Create your models here.
class StationStop(models.Model):
    stopcode = models.CharField(max_length = 10)
    stopname = models.CharField(max_length = 64)

    def __str__(self):
        return f"{self.stopname}"
