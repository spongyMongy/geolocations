from django.db import models


class Locations(models.Model):
    ip = models.GenericIPAddressField(unique=True)
    type = models.CharField(max_length=6)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    continent_code = models.CharField(max_length=2, default="NA")
    continent_name = models.CharField(max_length=20, default="Unknown")
    country_code = models.CharField(max_length=10, default="Unknown")
    country_name = models.CharField(max_length=70, default="Unknown")
    region_code = models.CharField(max_length=10, default="Unknown")
    region_name = models.CharField(max_length=50, default="Unknown")
    city = models.CharField(max_length=100, default="Unknown")
    zip = models.CharField(max_length=10, default="Unknown")

    def __str__(self):
        return self.ip

