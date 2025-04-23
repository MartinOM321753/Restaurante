
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}  # Evita exponer contraseñas en las respuestas

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            name=validated_data['name'],
            role=validated_data.get('role'),
        )
        user.set_password(validated_data['password'])  # Encripta la contraseña antes de guardarla
        user.save()
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['user_id'] = user.id
        token['role'] = user.role.name if user.role else None  # Añadir rol al token
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user_id'] = self.user.id
        data['role'] = self.user.role.name if self.user.role else None  # Añadir rol a la respuesta
        return data