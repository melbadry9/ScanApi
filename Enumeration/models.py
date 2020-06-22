import datetime
from django.db import models
from django.utils import timezone


# Create your models here.
class Domain(models.Model):
    name = models.CharField(max_length=255, unique=True)
    init_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Subdomain(models.Model):
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, db_index=True, unique=True, primary_key=True)
    http = models.BooleanField(default=False, auto_created=True, db_index=True)
    https = models.BooleanField(default=False, auto_created=True, db_index=True)
    init_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    #def was_init_recently(self, days):
    #    return self.subdomain_init_date >= timezone.now() - datetime.timedelta(days=days)