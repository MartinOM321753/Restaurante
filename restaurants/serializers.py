from rest_framework import serializers
from django.db import transaction
from .models import Restaurant
from restaurant_images.models import Restaurant_image
from ratings.models import Rating
import base64
import binascii
from django.db.models import Avg



class RestaurantImageSerializer(serializers.ModelSerializer):
    image_base64 = serializers.CharField(write_only=True, required=True)
    data = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant_image
        fields = ['id', 'name', 'type', 'image_base64', 'data']

    def validate_image_base64(self, value):
        try:
            base64.b64decode(value)
        except (binascii.Error, ValueError):
            raise serializers.ValidationError("La imagen en base64 no es válida.")
        return value

    def create(self, validated_data):
        image_base64 = validated_data.pop('image_base64')
        validated_data['data'] = base64.b64decode(image_base64)
        return Restaurant_image.objects.create(**validated_data)

    def get_data(self, obj):
        return base64.b64encode(obj.data).decode('utf-8') if obj.data else None



class RestaurantSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()

    restaurant_image  = RestaurantImageSerializer(required=True)  # La imagen es obligatoria en creación

    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'address', 'phone', 'description', 'user', 'start_date', 'restaurant_image','average_rating']



    def get_average_rating(self, obj):
        avg_rating = Rating.objects.filter(restaurant=obj).aggregate(avg_score=Avg('score'))['avg_score']
        return round(avg_rating, 2) if avg_rating is not None else 0.0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacemos la imagen opcional solo para actualizaciones
        if self.context.get('request') and self.context['request'].method in ['PUT', 'PATCH']:
            self.fields['restaurant_image'].required = False

    def validate(self, data):
        # Validación adicional para asegurarse que en creación haya imagen
        if self.context['request'].method == 'POST' and 'restaurant_image' not in data:
            raise serializers.ValidationError({"restaurant_image": "La imagen es obligatoria para crear un restaurante."})
        return data

    def create(self, validated_data):
        if 'restaurant_image' not in validated_data:
            raise serializers.ValidationError({"restaurant_image": "La imagen es obligatoria."})

        image_data = validated_data.pop('restaurant_image')

        with transaction.atomic():
            restaurant = Restaurant.objects.create(**validated_data)

            # Procesamiento de la imagen (obligatoria en creación)
            if 'image_base64' not in image_data:
                raise serializers.ValidationError({"restaurant_image": "image_base64 es requerido para la imagen."})

            try:
                image_data['data'] = base64.b64decode(image_data['image_base64'])
            except (binascii.Error, ValueError):
                raise serializers.ValidationError({"restaurant_image": "La imagen en base64 no es válida."})

            image_data.pop('image_base64', None)
            # Aquí utilizamos el nombre correcto de la relación
            Restaurant_image.objects.create(restaurant=restaurant, **image_data)

        return restaurant

    def update(self, instance, validated_data):
        image_data = validated_data.pop('restaurant_image', None)

        with transaction.atomic():
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()

            if image_data:
                if 'image_base64' in image_data:
                    try:
                        image_data['data'] = base64.b64decode(image_data['image_base64'])
                    except (binascii.Error, ValueError):
                        raise serializers.ValidationError({"restaurant_image": "La imagen en base64 no es válida."})

                if hasattr(instance, 'restaurant_image'):
                    restaurant_image = instance.restaurant_image
                    for attr, value in image_data.items():
                        if attr != 'image_base64':
                            setattr(restaurant_image, attr, value)
                    restaurant_image.save()
                elif 'data' in image_data:
                    image_data.pop('image_base64', None)
                    Restaurant_image.objects.create(restaurant=instance, **image_data)

        return instance