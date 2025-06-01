from rest_framework import serializers
from .models import UserProfile, Recipe

class UserProfileSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    username = serializers.CharField(max_length=100)
    mood_history = serializers.ListField(child=serializers.DictField(), default=list)
    preferences = serializers.DictField(default=dict)

    def create(self, validated_data):
        instance = UserProfile(**validated_data)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class RecipeSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=200)
    ingredients = serializers.ListField(child=serializers.DictField(), default=list)
    taste = serializers.CharField(max_length=50)
    budget = serializers.CharField(max_length=10)

    def create(self, validated_data):
        instance = Recipe(**validated_data)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance