from rest_framework import serializers
from realapp.models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields="__all__"

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields ="__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        # fields=("name","price")
        # exclude=("name",)
        fields="__all__"
        # depth=1

    def to_representation(self, instance):
        represent =  super().to_representation(instance)
        represent['category']=CategorySerializer(instance.category).data
        represent['company']=CompanySerializer(instance.company).data
        return represent