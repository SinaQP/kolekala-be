from apps.core.serializers import ModelSerializer
from .models import Product, ProductCategory

from rest_framework import serializers


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data

class ProductCategorySerializer(serializers.ModelSerializer):
    parent_category = serializers.StringRelatedField()
    child_categories = RecursiveField(many=True, read_only=True)

    class Meta:
        model = ProductCategory
        fields = ['name', 'description', 'parent_category', 'child_categories']
