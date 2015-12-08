#!/usr/bin/env python 
#-*-coding=utf-8-*-

from django.db import models
from demo.transmethod.tabale_file  import get_now_time

# Create your models here.

class Sdmodel(models.Model):
    created = models.DateField(auto_now_add=True)
    created_time  = models.CharField(max_length=30, blank=True, default='')
    sdmethod = models.CharField(max_length=10, blank=True, default='')
    table = models.TextField()
    c = models.CharField(max_length=10, blank=True, default='')
    s = models.CharField(max_length=10, blank=True, default='')
    b = models.CharField(max_length=10, blank=True, default='')
    
    def __str__(self):              # __unicode__ on Python 2
        return self.sdmethod
    
    #class Meta:
       # ordering = ('created',)