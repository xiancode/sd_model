#!/usr/bin/env python 
#-*-coding=utf-8-*-


# from django.forms import widgets
from rest_framework import serializers
from demo.models import Sdmodel

class SdmodelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sdmodel
        fields = ('created','created_time','rand_fname','sdmethod','table','c','s','b')