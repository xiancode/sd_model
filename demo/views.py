#!/usr/bin/env python 
#-*-coding=utf-8-*-

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

# Create your views here.

#renderer_classes = (JSONRenderer, )

class SdViewSet(viewsets.ModelViewSet):
    '''
    
    '''
    #queryset = Sdmodel.objects.all().order_by('-sdmethod')
    queryset = Sdmodel.objects.all()
    serializer_class = SdmodelSerializer

class ApiViewSet(APIView):
    #renderer_classes = (JSONRenderer, )
    def post(self, request, format=None):
        serializer = SdmodelSerializer(data=request.data)
        if serializer.is_valid():
            #v_data = serializer.validated_data
            serializer.save()
            seria_data = serializer.data
            
            sdmethod = seria_data.get("sdmethod")
            table = seria_data.get("table")
            
            
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        



# @api_view(['GET', 'POST'])
# def sdapi_view(request):
#     if request.method == 'POST':
#         data  = request.data
#         content = {'user_count': 'admin','group':'stuff'}
#         #return Response({"message": "Got some data!", "data": request.data})
#         return Response(content)
#     return Response({"message": "Hello, world!"})


    
        