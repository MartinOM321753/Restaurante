from foods.serializers import FoodSerializer

from rest_framework import serializers

from sales_details.models import SaleDetail
from foods.models import Foods

class SaleDetailSerializer(serializers.ModelSerializer):
    food = serializers.PrimaryKeyRelatedField(queryset=Foods.objects.all())
    food_info = FoodSerializer(source='food', read_only=True)

    class Meta:
        model = SaleDetail
        fields = ['food', 'food_info', 'quantity', 'unit_price', 'subtotal']
        extra_kwargs = {
            'unit_price': {'required': False},
            'subtotal': {'required': False},
        }
