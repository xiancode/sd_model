#!/usr/bin/env python 
#-*-coding=utf-8-*-

import os
import logging
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from demo.serializers import SdmodelSerializer
from demo.models import Sdmodel
from demo.common.timefile import json_file,get_now_time,generate_file_from_timestr,random_num_str
from demo.sdmethod import sd_em,sd_fa,sd_pca,sd_apri
from demo.sdmethod.sd_method import get_all_sd_method

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view

from rest_framework import mixins
from rest_framework import generics

BASE_DIR =os.path.dirname(os.path.abspath(__file__))

logger = logging.getLogger('SD_API')
logger.setLevel(logging.INFO)
fh = logging.FileHandler(BASE_DIR + os.path.sep + "LOG" + os.path.sep + "SD_API.log")
fh.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

def model_cal(seria_data,sdmethod,save_filename,result_filename=None):
    '''
    
    '''
    cal_result={}
    if sdmethod  not in get_all_sd_method():
        cal_result['error'] = 'not found request ' + sdmethod + ' method. '
        return cal_result
    if sdmethod == "sd_em":
        try:
            cal_result = sd_em.sd_em(save_filename, result_filename)
        except Exception,e:
            cal_result['cal_error']  = "sd_em method cal error"
            logging.error("method  sd_em",e)
    elif sdmethod == "sd_fa":
        try:
            c  = seria_data.get("c")
        except Exception,e:
            cal_result["para_error"] = "can not  get 'c' from request"        
        try:
            cal_result = sd_fa.sd_fa(save_filename, int(c), result_name=None)
        except Exception,e:
            cal_result["cal_error"] = "sd_fa method cal error"
            logging.error("method  sd_fa",e)
    elif sdmethod == "sd_pca":
        try:
            c  = seria_data.get("c")
        except Exception,e:
            cal_result["para_error"] = "can not  get 'c' from request"
        try:
            cal_result = sd_pca.sd_pca(save_filename, int(c), result_name=None)
        except Exception,e:
            cal_result["cal_error"] = "sd_pca  method cal error"
            logging.error("method  sd_pca",str(e))
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
        except Exception,e:
            cal_result["cal_error"] = "sd_apri  method cal error"
            logging.error("method  sd_apri",e)
        else:
            cal_result["para_error"] = "can not find method  to cal"
    return cal_result
    
class SdViewSet(viewsets.ModelViewSet):
    '''
    
    '''
    #queryset = Sdmodel.objects.all().order_by('-sdmethod')
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    queryset = Sdmodel.objects.all()
    serializer_class = SdmodelSerializer
    
@api_view(['GET','POST'])
def sdcal_list(request):
    """
    
    """
    if request.method == 'GET':
        querysets = Sdmodel.objects.all()
        serializer = SdmodelSerializer(querysets,many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = SdmodelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CalList(APIView):
    '''
    
    '''
    def get(self,request,format=None):
        querysets = Sdmodel.objects.all()
        serializer = SdmodelSerializer(querysets,many=True)
        return Response(serializer.data)
    
    def post(self,request,format=None):
        serializer = SdmodelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CalListOne(mixins.ListModelMixin,
                                 mixins.CreateModelMixin,
                                 generics.GenericAPIView):
    queryset = Sdmodel.objects.all()
    serializer_class = SdmodelSerializer
    
    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)    
    

class ApiViewSet(APIView):
    authentication_classes = (BasicAuthentication,SessionAuthentication )
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        table = request.data['table']
        result_filename = None
        data = request.data.copy()
        logger.info("New request")
        data["created_time"] = get_now_time()
        data['rand_fname'] = random_num_str()
        serializer = SdmodelSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            seria_data = serializer.data
            date_str = seria_data.get("created")
            time_str = seria_data.get("created_time")
            sdmethod = seria_data.get("sdmethod")
            rand_fname = seria_data.get("rand_fname")
            save_filename = generate_file_from_timestr(date_str,time_str, BASE_DIR + os.path.sep + "data",rand_fname)
            json_file(table, save_filename)
            cal_result = model_cal(seria_data, sdmethod, save_filename, result_filename)
            return Response(cal_result, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


    
        