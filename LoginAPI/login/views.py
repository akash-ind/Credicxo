from django.shortcuts import render
from django.contrib.auth.models import User
from login.serializers import UserSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import Group
from .serializers import UserSerializer
from rest_framework.response import Response
# Create your views here.


def genMissingErros(dct, values):
    """
    function to dictionary for required values
    """
    errors = {}
    for value in values:
        if not dct.get(value):
            errors[value] = "required"
    return errors

@csrf_exempt
def createUser(request):
    """
    endpoint for creating Student, Teacher, admin 
    """
    required_values = ["first_name", "email", "last_name",
    "username", "type", "password"]
    errors = genMissingErros(request.POST, required_values)
    if errors:
        return JsonResponse(errors)
    first_name = request.POST["first_name"]
    last_name = request.POST["last_name"]
    username = request.POST["username"]
    email = request.POST["email"]
    password = request.POST["password"]
    type = request.POST["type"]
    user = User(first_name=first_name,
                last_name=last_name, email = email, username = username)
    user.set_password(password)
    group = Group.objects.get(name=type)
    try:
        user.save()
        user.groups.add(group)
    except Exception as e:
        return JsonResponse({"error": str(e)})
    return JsonResponse({"done":"user created successfully"})



class ListUsers(ListAPIView):
    """
    Lists users based on whether request came from Student, Teacher or Admin
    """ 
    permission_classes = [IsAuthenticated]
    
    def list(self, request, *args, **kwargs):
        user = request.user
        queryset = User.objects.none()
        admin = Group.objects.get(name = "admin")
        student = Group.objects.get(name = "student")
        teacher = Group.objects.get(name = "teacher")
        if admin in user.groups.all():
            queryset = User.objects.all()
        elif teacher in user.groups.all():
            student_group = Group.objects.get(name="student")
            queryset = student_group.user_set.all()
        elif student in user.groups.all():
            queryset = User.objects.filter(username = user.username)
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)



def ret_user(request):
    user = request.user
    print(user)
    return JsonResponse({"user":user})