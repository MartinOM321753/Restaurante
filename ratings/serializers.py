from rest_framework import serializers
from .models import Rating
from decimal import Decimal

from django.utils import timezone


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'
        read_only_fields = ['start_date']

    def validate_score(self, value):
        allowed_scores = [Decimal(str(x)) for x in (0, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5)]
        if value not in allowed_scores:
            raise serializers.ValidationError(f"La calificación debe de ser una de las siguientes:  {allowed_scores}")
        return value

    def create(self, validated_data):
        validated_data['start_date'] = timezone.now()
        return super().create(validated_data)


#NGROW