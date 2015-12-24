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
from demo.common.timefile import json_file,get_now_time,generate_file_from_timestr
from demo.sdmethod import sd_em,sd_fa,sd_pca,sd_apri

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

BASE_DIR =os.path.dirname(os.path.abspath(__file__))

logger = logging.getLogger('SD_API')
logger.setLevel(logging.INFO)
fh = logging.FileHandler(BASE_DIR + os.path.sep + "LOG" + os.path.sep + "SD_API.log")
fh.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

class SdViewSet(viewsets.ModelViewSet):
    '''
    
    '''
    #queryset = Sdmodel.objects.all().order_by('-sdmethod')
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    queryset = Sdmodel.objects.all()
    serializer_class = SdmodelSerializer

class ApiViewSet(APIView):
    authentication_classes = (BasicAuthentication,SessionAuthentication )
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        table = request.data['table']
        result_filename = None
        data = request.data.copy()
        logger.info("New request")
        data["created_time"] = get_now_time()
        serializer = SdmodelSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            seria_data = serializer.data
            date_str = seria_data.get("created")
            time_str = seria_data.get("created_time")
            sdmethod = seria_data.get("sdmethod")
            
            save_filename = generate_file_from_timestr(date_str,time_str, BASE_DIR + os.path.sep + "data")
            json_file(table, save_filename)
            
            cal_result = {}
            #logging.info("cal...........")
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


    
        