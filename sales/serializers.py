from rest_framework import serializers
from django.db import transaction
from .models import Sale
from sales_details.models import SaleDetail
from sales_details.serializers import SaleDetailSerializer


# serializers.py
from rest_framework import serializers
from .models import Sale
from restaurants.models import Restaurant  # ajusta si el modelo está en otro archivo
from restaurants.serializers import RestaurantSerializer


class SaleSerializer(serializers.ModelSerializer):
    details = SaleDetailSerializer(many=True)
    restaurant = serializers.PrimaryKeyRelatedField(queryset=Restaurant.objects.all())



    class Meta:
        model = Sale
        fields = ['id', 'restaurant', 'date', 'total', 'details', 'user']
        read_only_fields = ['id', 'date', 'total', 'user']

    def validate(self, data):
        details = data.get('details')
        if not details:
            raise serializers.ValidationError("Debe agregar al menos un alimento en la venta.")

        for detail in details:
            food = detail.get('food')
            quantity = detail.get('quantity')

            if quantity is None or quantity <= 0:
                raise serializers.ValidationError(f"La cantidad para el alimento {food} debe ser mayor que cero.")

            if food.stock < quantity:
                raise serializers.ValidationError(f"No hay suficiente stock disponible para el alimento '{food.name}'. Stock disponible: {food.stock}")

        return data

    @transaction.atomic
    def create(self, validated_data):
        details_data = validated_data.pop('details')
        user = self.context['request'].user

        sale = Sale.objects.create(user=user, **validated_data)

        total = 0
        sale_details = []

        for detail_data in details_data:
            food = detail_data['food']
            quantity = detail_data['quantity']
            unit_price = food.price
            subtotal = quantity * unit_price

            # Actualizar stock
            food.stock -= quantity
            food.save()

            sale_detail = SaleDetail(
                sale=sale,
                food=food,
                quantity=quantity,
                unit_price=unit_price,
                subtotal=subtotal
            )
            sale_details.append(sale_detail)
            total += subtotal

        SaleDetail.objects.bulk_create(sale_details)

        sale.total = total
        sale.save()

        return sale

