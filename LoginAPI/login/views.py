from django.shortcuts import render
from django.contrib.auth.models import User
from login.serializers import UserSerializer
from django.http import JsonResponse
# Create your views here.


def genMissingErros(dct, values):
    """This function checks the dictionary for required values"""
    errors = {}
    for value in values:
        if not dct.get(value):
            errors[value] = "required"
    return errors


def createUser(request):
    """
    endpoint for creating Student, Teacher, admin 
    """
    required_values = ["first_name", "last_name", "type"]
    errors = genMissingErros(request.POST, required_values)
    if errors:
        return JsonResponse(errors)
    first_name = request.POST["first_name"]
    last_name = request.POST["last_name"]
    type = request.POST["type"]
    user = User(first_name=first_name,
                last_name=last_name)
    print(type)
    user.save()
    return JsonResponse({done: True})

