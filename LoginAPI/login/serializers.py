from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    """For serializing User Model"""
    class meta:
        model = User
        fields = "__all__"
