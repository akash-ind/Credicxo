from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.utils import model_meta
import traceback
from django.contrib.auth.models import Group

def required(value):
    """Checks if the value is specified or not"""
    if value is None:
        raise serializers.ValidationError('This field is required')

def check(value):
    """Checks if the correct type value specified"""
    if value != "student" and value != "teacher" and value != "admin":
        raise serializers.ValidationError("Wrong Type Specified")

class UserSerializer(serializers.ModelSerializer):
    """For serializing User Model 
    type field data necessary to create objects""" 
    type = serializers.CharField(validators = [required, check], write_only =True)
    types = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'type', 'types',
        'password', 'groups']
        extra_kwargs = {'password':{'write_only':True}, 
        'groups':{'write_only':True}}


    def get_types(self, obj):
        names = []
        for group in obj.groups.all():
            names.append(group.name)
        return names

    def create(self, validated_data):
        """
        Extended create method to include groups teachers, 
        student and Admin
        """

        ModelClass = self.Meta.model
        type = validated_data.pop("type")
        #This is to remove the field non existing to user
        info = model_meta.get_field_info(ModelClass)
        many_to_many = {}
        for field_name, relation_info in info.relations.items():
            if relation_info.to_many and (field_name in validated_data):
                many_to_many[field_name] = validated_data.pop(field_name)

        try:
            instance = ModelClass._default_manager.create(**validated_data)
        except TypeError:
            tb = traceback.format_exc()
            msg = ('Got a `TypeError` when calling `%s.%s.create()`. '
                'This may be because you have a writable field on the '
                'serializer class that is not a valid argument to '
                '`%s.%s.create()`. You may need to make the field '
                'read-only, or override the %s.create() method to handle '
                'this correctly.\nOriginal exception was:\n %s'%(
                    ModelClass.__name__,
                    ModelClass._default_manager.name,
                    ModelClass.__name__,
                    ModelClass._default_manager.name,
                    self.__class__.__name__,
                    tb
                )
            )
            raise TypeError(msg)

        # Save many-to-many relationships after the instance is created.
        groups = []
        if type == "student":
            group = Group.objects.get(name = "student")
            groups.append(group)
        elif type == "teacher":
            group = Group.objects.get(name = "teacher")
            groups.append(group)
        elif type == "admin":
            group = Group.objects.get(name = "admin")
            groups.append(group)
        many_to_many["groups"] = groups
        if many_to_many:
            for field_name, value in many_to_many.items():
                field = getattr(instance, field_name)
                field.set(value)
        return instance

