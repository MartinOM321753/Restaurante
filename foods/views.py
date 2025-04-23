from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.permissions import AllowAny

from .models import Foods
from .serializers import FoodSerializer
class FoodsViewSet(viewsets.ModelViewSet):
    queryset = Foods.objects.all().prefetch_related('image')
    serializer_class = FoodSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


class FindFoodsByMenu(APIView):
    permission_classes = [AllowAny]

    def get(self, request, menu_id, *args, **kwargs):
        foods = Foods.objects.filter(menu_id=menu_id)
        serializer = FoodSerializer(foods, many=True)
        return Response(serializer.data, status=200)