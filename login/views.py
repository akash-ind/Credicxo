from django.shortcuts import render
from django.contrib.auth import get_user_model
from login.serializers import UserSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import Group
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.tokens import default_token_generator
# Create your views here.

User = get_user_model()


def genMissingErros(dct, values):
    """
    function to dictionary for required values
    """
    errors = {}
    for value in values:
        if not dct.get(value):
            errors[value] = "required"
    return errors



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


class CreateUser(CreateAPIView):
    """
    Create Users on whether the request came from Student, Teacher, Admin
    """
    permission_classes = [IsAuthenticated]
    allowed_methods = ["POST"]

    def create(self, request, *args, **kwargs):
        user = request.user
        admin = Group.objects.get(name = "admin")
        teacher = Group.objects.get(name = "teacher")
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if admin in user.groups.all():
            pass
        elif teacher in user.groups.all():
            if request.data.get("type") != "student":
                return Response({"error":"Operation not allowed"},
                status = status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"error":"Operation not allowed"},
                    status = status.HTTP_401_UNAUTHORIZED)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



class ForgotPassword(APIView):
    """
    Takes in username and sends a unique token. Token is stored in the session.
    And from session token is verified
    """
    def post(self, request, format = None):
        errors = genMissingErros(request.data, ['username'])
        if errors:
            return Response(errors, status = status.HTTP_400_BAD_REQUEST)
        username = request.data['username']
        user = User.objects.get(username=username)
        token = default_token_generator.make_token(user)
        request.session[token] = user.pk
        return Response({"token":token}, status = status.HTTP_200_OK)



class ChangePassword(APIView):
    """
    Takes POST request with 
    new password and token and change if token is valid
    """

    def post(self, request, format = None):
        errors = genMissingErros(request.data, ["new_password", "token"])
        if errors:
            return Response(errors, status = status.HTTP_400_BAD_REQUEST)
        token = request.data["token"]
        pk = request.session.get(token, None)
        if pk is None:
            return Response({"error":"Token not valid"}, 
            status = status.HTTP_406_NOT_ACCEPTABLE)
        user = User.objects.get(pk = pk)
        user.set_password(request.data["new_password"])
        del request.session[token]
        return Response({"done":"Password reset successfully"}, 
        status = status.HTTP_200_OK)

        
