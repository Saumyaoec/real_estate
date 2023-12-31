from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Tenant, TenantAssignment
from .serializers import TenantSerializer, TenantAssignmentSerializer

class TenantListCreateAPIView(APIView):
    def get(self, request):
        tenants = Tenant.objects.all()
        serializer = TenantSerializer(tenants, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TenantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TenantAssignmentListCreateAPIView(APIView):
    def get(self, request):
        tenant_assignments = TenantAssignment.objects.all()
        serializer = TenantAssignmentSerializer(tenant_assignments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TenantAssignmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
