from django.db import models

class Company(models.Model):
    name    = models.CharField(max_length=45)
    country = models.CharField(max_length=45)
    city    = models.CharField(max_length=45)

    class Meta:
        db_table = "companies"