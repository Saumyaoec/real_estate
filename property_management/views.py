from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Property
from .serializers import PropertySerializer
from authentications.permissions import IsAuthenticated, IsAdmin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView


class PropertyCreateAPIView(APIView):
    def get(self, request):
        return render(request, 'property_create.html', {'request': request})

    def post(self, request):
        serializer = PropertySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class PropertyListAPIView(APIView):
    def get(self, request):
        properties = Property.objects.all()
        return render(request, 'property_list.html', {'properties': properties})


class UnitListCreateAPIView(APIView):
    def get(self, request, property_id):
        units = Unit.objects.filter(property_id=property_id)
        serializer = UnitSerializer(units, many=True)
        return Response(serializer.data)

    def post(self, request, property_id):
        serializer = UnitSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(property_id=property_id)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class UnitDetailAPIView(APIView):
    def get(self, request, property_id, unit_id):
        unit = get_object_or_404(Unit, property_id=property_id, id=unit_id)
        serializer = UnitSerializer(unit)
        return Response(serializer.data)

    def put(self, request, property_id, unit_id):
        unit = get_object_or_404(Unit, property_id=property_id, id=unit_id)
        serializer = UnitSerializer(unit, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, property_id, unit_id):
        unit = get_object_or_404(Unit, property_id=property_id, id=unit_id)
        unit.delete()
        return Response(status=204)
