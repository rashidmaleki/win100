from django.shortcuts import render
from rest_framework import generics
from .serializers import DepartmansSerializer
from support.models import Departman

# Create your views here.


class DepartmansViewSet(generics.ListAPIView):
    serializer_class = DepartmansSerializer
    queryset = Departman.objects.all()
