from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer

from .models import Role

from .serializers import RoleSerializer

# Create your views here.

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    renderer_classes = [JSONRenderer]