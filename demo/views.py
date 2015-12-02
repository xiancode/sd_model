#!/usr/bin/env python 
#-*-coding=utf-8-*-
import json
import os
from django.shortcuts import render
from rest_framework import viewsets
from demo.serializers import SdmodelSerializer
from demo.models import Sdmodel
from rest_framework.response import Response

from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView

from django.http import Http404
from rest_framework import status

from demo.transmethod.tabale_file import json_file,generate_file_from_time
from demo.sdmethod import sd_em

from django.utils import  timezone
import datetime
from django.utils.timezone import utc

# Create your views here.

#renderer_classes = (JSONRenderer, )

BASE_DIR =os.path.dirname(os.path.abspath(__file__))

class SdViewSet(viewsets.ModelViewSet):
    '''
    
    '''
    #queryset = Sdmodel.objects.all().order_by('-sdmethod')
    queryset = Sdmodel.objects.all()
    serializer_class = SdmodelSerializer

class ApiViewSet(APIView):
    #renderer_classes = (JSONRenderer, )
    def post(self, request, format=None):
        table = request.data['table']
        current = datetime.datetime.utcnow().replace(tzinfo=utc)
        current = timezone.localtime(current)
        #save_filename = BASE_DIR+"/data/table_upload.txt"
        save_filename = generate_file_from_time(current, BASE_DIR + os.path.sep + "data")
        #result_filename = save_filename[:-4] + "_result.dat"
        result_filename = None
        json_file(table, save_filename)
        serializer = SdmodelSerializer(data=request.data)
        if serializer.is_valid():
            #now = datetime.datetime.utcnow().replace(tzinfo=utc)
            #now = timezone.localtime(now)
            #v_data = serializer.validated_data
            serializer.save()
            seria_data = serializer.data
            sdmethod = seria_data.get("sdmethod")
            cal_result = {}
            if sdmethod == "sd_em":
                cal_result = sd_em.sd_em(save_filename, result_filename)
            elif sdmethod == "sd_fa":
                try:
                    c = sdmethod = seria_data.get("c")
                    pass
                except Exception,e:
                    cal_result["error"] = "can not  get 'c' from request"
            elif sdmethod == "sd_pac":
                pass
            elif sdmethod == "aprior":
                pass
            
            #return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(cal_result, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

# @api_view(['GET', 'POST'])
# def sdapi_view(request):
#     if request.method == 'POST':
#         data  = request.data
#         content = {'user_count': 'admin','group':'stuff'}
#         #return Response({"message": "Got some data!", "data": request.data})
#         return Response(content)
#     return Response({"message": "Hello, world!"})


    
        