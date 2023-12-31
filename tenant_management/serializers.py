from rest_framework import serializers
from .models import Tenant, TenantAssignment

class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = ['id', 'user', 'name', 'address']

class TenantAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantAssignment
        fields = ['id', 'tenant', 'unit', 'agreement_end_date', 'monthly_rent_date']
