from django.shortcuts import render

# Create your views here.
import json

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate

@csrf_exempt
def register_user(request):
    if request.method == "POST":
        data = json.loads(request.body)

        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if User.objects.filter(username=username).exists():
            return JsonResponse(
                {"error": "Username already exists"},
                status=400,
            )

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )

        return JsonResponse({
            "message": "Registration Successful!",
            "username": user.username,
        })

    return JsonResponse(
        {"error": "Invalid request"},
        status=400,
    )

@csrf_exempt
def login_user(request):
    if request.method == "POST":
        data = json.loads(request.body)

        username = data.get("username")
        password = data.get("password")

        user = authenticate(
            username=username,
            password=password,
        )

        if user is not None:
            return JsonResponse({
                "message": "Login Successful",
                "username": user.username,
            })

        return JsonResponse(
            {"error": "Invalid username or password"},
            status=400,
        )

    return JsonResponse(
        {"error": "Invalid request"},
        status=400,
    )