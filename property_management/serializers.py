from rest_framework import serializers
from .models import Property, Unit

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        exclude = ['owner']
    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user  
        return super().create(validated_data)
        
class PropertyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ['id', 'property', 'rent_cost', 'unit_type']
        read_only_fields = ['id']
