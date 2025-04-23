from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Rating
from .serializers import RatingSerializer

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
