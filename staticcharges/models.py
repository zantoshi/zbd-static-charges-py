from django.db import models
from django.forms import CharField


class StaticCharge(models.Model):
    min_amount = models.CharField(max_length=50)
    max_amount = models.CharField(max_length=50)
    description = models.CharField(max_length=225)
    identifier = models.CharField(max_length=500, blank=True)
    ext_static_charge_id = models.CharField(max_length=50)
    lnurlp = models.CharField(max_length=250)