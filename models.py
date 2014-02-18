from django.db import models

class SarpyWarrant(models.Model):
    last = models.CharField(max_length=50, null=True, blank=True)
    rest = models.CharField(max_length=50, null=True, blank=True)
    dob = models.DateField()
    race = models.CharField(max_length=30, null=True, blank=True)
    issued = models.CharField(max_length=50, null=True, blank=True)
    type = models.CharField(max_length=50, null=True, blank=True)
    charge = models.TextField(max_length=255, null=True, blank=True)

class PottWarrant(models.Model):
    last = models.CharField(max_length=50, null=True, blank=True)
    first = models.CharField(max_length=50, null=True, blank=True)
    date_conf = models.CharField(max_length=25, null=True, blank=True)
    time_conf = models.CharField(max_length=25, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    height = models.CharField(max_length=15, null=True, blank=True)
    weight = models.CharField(max_length=15, null=True, blank=True)
    sex = models.CharField(max_length=15, null=True, blank=True)
    race = models.CharField(max_length=30, null=True, blank=True)
    charges = models.TextField(null=True, blank=True)
    bond = models.CharField(max_length=125, null=True, blank=True)


class Inmate(models.Model):
    last = models.CharField(max_length=50)
    rest = models.CharField(max_length=50)
    crime = models.TextField()
    age = models.IntegerField()
    sex = models.CharField(max_length=1)
    race = models.CharField(max_length=1)
    height = models.CharField(max_length=5, null=True, blank=True)
    weight = models.CharField(max_length=5, null=True, blank=True)
    facility = models.CharField(max_length=60, null=True, blank=True)
    admissiondate = models.DateField()
    admissiontime = models.TimeField()
    bond = models.CharField(max_length=60, null=True, blank=True)
    fine = models.CharField(max_length=60, null=True, blank=True)
    freshness = models.CharField(max_length=10)

class Name(models.Model):
    first = models.CharField(max_length=50, null=True, blank=True)
    last = models.CharField(max_length=50)

class Subscribers(models.Model):
    email = models.EmailField()
