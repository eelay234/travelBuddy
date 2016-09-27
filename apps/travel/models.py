from __future__ import unicode_literals
from django.db import models
import re
from django.http import HttpResponse
from django.contrib import messages
import datetime

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=45)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __unicode__(self):
        return self.name

class Trip(models.Model):
    destination = models.CharField(max_length=45)
    description = models.CharField(max_length=100)
    planner = models.ForeignKey("User", related_name="planner")
    turists = models.ManyToManyField(User, related_name="turists")
    from_date = models.DateField(default=datetime.date.today)
    to_date = models.DateField(default=datetime.date.today)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __unicode__(self):
        return self.destination
