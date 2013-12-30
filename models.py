from django.db import models

class SarpyWarrant(models.Model):
    last = models.CharField(max_length=50, null=True, blank=True)
    rest = models.CharField(max_length=50, null=True, blank=True)
    dob = models.DateField()
    eyes = models.CharField(max_length=4, null=True, blank=True)
    hair = models.CharField(max_length=4, null=True, blank=True)
    sex = models.CharField(max_length=1, null=True, blank=True)
    race = models.CharField(max_length=4, null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=50, null=True, blank=True)
    apt = models.CharField(max_length=20, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=2, null=True, blank=True)
    issued = models.DateField(null=True, blank=True)
    type = models.CharField(max_length=50, null=True, blank=True)
    court = models.CharField(max_length=50, null=True, blank=True)
    agency = models.CharField(max_length=50, null=True, blank=True)
    due = models.CharField(max_length=50, null=True, blank=True)
    crime = models.TextField(max_length=255, null=True, blank=True)
    

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

