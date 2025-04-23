from rest_framework import viewsets
from .models import Sale
from .serializers import SaleSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection
from rest_framework.permissions import AllowAny

class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        restaurant_id = self.request.query_params.get('restaurant_id')
        if restaurant_id:
            queryset = queryset.filter(restaurant_id=restaurant_id)
        return queryset


class MostSoldFoodsView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, restaurant_id):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    f.name AS food_name,
                    SUM(d.quantity) AS total_quantity_sold
                FROM sales_details_saledetail d
                JOIN sales_sale s ON d.sale_id = s.id
                JOIN foods_foods f ON d.food_id = f.id
                WHERE s.restaurant_id = %s
                GROUP BY f.name
                ORDER BY total_quantity_sold DESC;
            """, [restaurant_id])
            results = cursor.fetchall()

        data = [
            {"food_name": row[0], "total_quantity_sold": row[1]}
            for row in results
        ]
        return Response(data)

class MostSoldFoodsGlobalView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    f.name AS food_name,
                    SUM(d.quantity) AS total_quantity_sold
                FROM sales_details_saledetail d
                JOIN sales_sale s ON d.sale_id = s.id
                JOIN foods_foods f ON d.food_id = f.id
                GROUP BY f.name
                ORDER BY total_quantity_sold DESC;
            """)
            results = cursor.fetchall()

        data = [
            {"food_name": row[0], "total_quantity_sold": row[1]}
            for row in results
        ]
        return Response(data)

class SalesByRestaurantView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, restaurant_id):
        sales = Sale.objects.filter(restaurant_id=restaurant_id).order_by('-date')
        serializer = SaleSerializer(sales, many=True)
        return Response(serializer.data)

class SalesByUserView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, user_id):
        sales = Sale.objects.filter(user_id=user_id).order_by('-date')
        serializer = SaleSerializer(sales, many=True)
        return Response(serializer.data)
