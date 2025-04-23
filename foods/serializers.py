from rest_framework import serializers
from django.db import transaction
from .models import Foods
from food_images.models import FoodImage
import base64
import binascii


class FoodImageSerializer(serializers.ModelSerializer):
    image_base64 = serializers.CharField(write_only=True, required=True)
    data = serializers.SerializerMethodField()

    class Meta:
        model = FoodImage
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
        return FoodImage.objects.create(**validated_data)

    def get_data(self, obj):
        return base64.b64encode(obj.data).decode('utf-8') if obj.data else None


class FoodSerializer(serializers.ModelSerializer):
    restaurant_id = serializers.SerializerMethodField()

    image = FoodImageSerializer(required=True)  # Mantenemos required=True para validación inicial

    def get_restaurant_id(self, obj):
        return obj.menu.restaurants_id if obj.menu else None
    class Meta:
        model = Foods
        fields = ['id', 'menu', 'name', 'description', 'price', 'image','stock','restaurant_id']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacemos la imagen opcional solo para updates
        if self.context.get('request') and self.context['request'].method in ['PUT', 'PATCH']:
            self.fields['image'].required = False

    def validate(self, data):
        # Validación adicional para asegurar que en creación haya imagen
        if self.context['request'].method == 'POST' and 'image' not in data:
            raise serializers.ValidationError({"image": "La imagen es obligatoria para crear una comida."})
        return data

    def create(self, validated_data):
        if 'image' not in validated_data:
            raise serializers.ValidationError({"image": "La imagen es obligatoria."})

        image_data = validated_data.pop('image')

        with transaction.atomic():
            food = Foods.objects.create(**validated_data)

            # Procesamiento de la imagen (obligatoria en creación)
            if 'image_base64' not in image_data:
                raise serializers.ValidationError({"image": "image_base64 es requerido para la imagen."})

            try:
                image_data['data'] = base64.b64decode(image_data['image_base64'])
            except (binascii.Error, ValueError):
                raise serializers.ValidationError({"image": "La imagen en base64 no es válida."})

            image_data.pop('image_base64', None)  # <- Corregido aquí
            FoodImage.objects.create(food=food, **image_data)

        return food

    def update(self, instance, validated_data):
        image_data = validated_data.pop('image', None)

        with transaction.atomic():
            # Actualización de campos básicos
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()

            # Lógica de actualización de imagen (opcional)
            if image_data:
                if 'image_base64' in image_data:
                    try:
                        image_data['data'] = base64.b64decode(image_data['image_base64'])
                    except (binascii.Error, ValueError):
                        raise serializers.ValidationError({"image": "La imagen en base64 no es válida."})

                if hasattr(instance, 'image'):
                    food_image = instance.image
                    for attr, value in image_data.items():
                        if attr != 'image_base64':
                            setattr(food_image, attr, value)
                    food_image.save()
                elif 'data' in image_data:
                    image_data.pop('image_base64', None)
                    FoodImage.objects.create(food=instance, **image_data)

        return instance
