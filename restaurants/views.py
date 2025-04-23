from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework import permissions
from .models import Restaurant
from .serializers import RestaurantSerializer
from rest_framework.permissions import AllowAny

# Create your views here.

class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    renderer_classes = [JSONRenderer]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return super().get_permissions()

class findByUser(APIView):
    permission_classes = [AllowAny]

    def get(self, request, user_id, *args, **kwargs):
        restaurants = Restaurant.objects.filter(user=user_id)
        serializer = RestaurantSerializer(restaurants, many=True)
        return Response(serializer.data, status=200)

class getFiveLatest(ListAPIView):
    serializer_class = RestaurantSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Restaurant.objects.order_by('-id')[:5]
