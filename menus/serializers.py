from rest_framework import serializers
from .models import Menu
from foods.serializers import FoodSerializer  # Importar el serializador de Food

class MenuSerializer(serializers.ModelSerializer):
    foods = FoodSerializer(many=True, read_only=True)  # Agregar Food dentro de cada menú

    class Meta:
        model = Menu
        fields = '__all__'
