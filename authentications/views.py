from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from .permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect, reverse
from .models import *
from .serializers import *
from .authentication import *


class SignupAPI(APIView):
    def get(self, request):
        return render(request, 'register.html')
    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            data = user.sign_in_with_email_and_password(
                user.email, request.data["password"]
            )
            serializer = UserAuthSerializer(instance=user, context={"request": request})
            context = {**serializer.data, **data, 'template_name': 'login.html'} 
            return redirect(reverse('login'))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPI(APIView):
    def get(self, request):
        return render(request, 'login.html')
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = data["user"]
        res = user.sign_in_with_email_and_password(data["email"], data["password"])
        serializer = UserAuthSerializer(user, context={"request": request})
        context = {**serializer.data, **res}
        # return redirect(reverse('dashboard'))
        return Response(context)


