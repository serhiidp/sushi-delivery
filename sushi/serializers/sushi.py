from rest_framework import serializers

from ..models.sushi import Category, Sushi


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class SushiSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Sushi
        fields = "__all__"
