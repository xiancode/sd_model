#!/usr/bin/env python 
#-*-coding=utf-8-*-

from django.db import models

# Create your models here.

class Sdmodel(models.Model):
    created = models.DateField(auto_now_add=True)
    sdmethod = models.CharField(max_length=100, blank=True, default='')
    table = models.TextField()
    
    def __str__(self):              # __unicode__ on Python 2
        return self.table
    
    #class Meta:
       # ordering = ('created',)