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

from demo.transmethod.tabale_file import json_file,generate_file_from_time,get_now_time,generate_file_from_timestr
from demo.sdmethod import sd_em,sd_fa,sd_pca,sd_apri

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
        #current = datetime.datetime.utcnow().replace(tzinfo=utc)
        #current = timezone.localtime(current)
        #save_filename = BASE_DIR+"/data/table_upload.txt"
        
        #result_filename = save_filename[:-4] + "_result.dat"
        result_filename = None
       
        data = request.data.dict()
        data["created_time"] = get_now_time()
        serializer = SdmodelSerializer(data=data)
        if serializer.is_valid():
            #now = datetime.datetime.utcnow().replace(tzinfo=utc)
            #now = timezone.localtime(now)
            #v_data = serializer.validated_data
            serializer.save()
            seria_data = serializer.data
            date_str = seria_data.get("created")
            time_str = seria_data.get("created_time")
            save_filename = generate_file_from_timestr(date_str,time_str, BASE_DIR + os.path.sep + "data")
            json_file(table, save_filename)
            sdmethod = seria_data.get("sdmethod")
            cal_result = {}
            if sdmethod == "sd_em":
                try:
                    cal_result = sd_em.sd_em(save_filename, result_filename)
                except Exception,e:
                    cal_result['cal_error']  = "sd_em method cal error"
            elif sdmethod == "sd_fa":
                try:
                    c  = seria_data.get("c")
                except Exception,e:
                    cal_result["para_error"] = "can not  get 'c' from request"
                    
                try:
                    cal_result = sd_fa.sd_fa(save_filename, int(c), result_name=None)
                except Exception,e:
                    cal_result["cal_error"] = "sd_fa method cal error"
            elif sdmethod == "sd_pca":
                try:
                    c  = seria_data.get("c")
                except Exception,e:
                    cal_result["para_error"] = "can not  get 'c' from request"
                    
                try:
                    cal_result = sd_pca.sd_pca(save_filename, int(c), result_name=None)
                except Exception,e:
                    cal_result["cal_error"] = "sd_pca  method cal error"
            elif sdmethod == "sd_apri":
                try:
                    c  = seria_data.get("c")
                except Exception,e:
                    cal_result["para_error"] = "can not  get 'c' from request"
                
                try:
                    b  = seria_data.get("b")
                except Exception,e:
                    cal_result["para_error"] = "can not  get 'b' from request"
                
                try:
                    s  = seria_data.get("s")
                except Exception,e:
                    cal_result["para_error"] = "can not  get 's' from request"
                    
                try:
                    cal_result = sd_apri.sd_apri_main(save_filename, b, s, c,result_name=None)
                    #cal_result = sd_pca.sd_pca(save_filename, int(c), result_name=None)
                except Exception,e:
                    cal_result["cal_error"] = "sd_apri  method cal error"
            else:
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


    
        