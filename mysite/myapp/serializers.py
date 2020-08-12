# myapp/serializers.py
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import *


# Serializers define the API representation.
class GeneralSerializer(serializers.ModelSerializer):
    class Meta:
        model = None
        fields = '__all__'


class V2OfUsersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = V2OfUsers
        fields = ('firstname', 'lastname', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user


class MeasurementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurements
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(MeasurementsSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.query_params.get('fields'):
            fields = request.query_params.get('fields')
            if fields:
                fields = fields.split(',')
                allowed = set(fields)
                existing = set(self.fields.keys())
                for field_name in existing - allowed:
                    self.fields.pop(field_name)


# Serializer for Counting Providers
# and Network Type e.g 2G, 3G, 4G


class CountSerializer(serializers.Serializer):
    key = serializers.CharField(max_length=20)
    value = serializers.IntegerField()

# Serializer for Mobile Operating System


class OperatingSystemSerializer(serializers.ModelSerializer):
    value = serializers.CharField(max_length=30)
    key = serializers.CharField(source='versionname', max_length=30)

    class Meta:
        model = Measurements
        fields = ('key', 'value')


# Serializer for Vendors


class VendorsSerializer(serializers.ModelSerializer):
    value = serializers.CharField(max_length=30)
    key = serializers.CharField(source='devicemanufacturer', max_length=30)

    class Meta:
        model = Measurements
        fields = ('key', 'value')


# General Serializer for DownLink and UpLink for all
# Providers and Network Types with date range parameters

class GlobalSerializer(serializers.Serializer):
    key = serializers.CharField(max_length=20)
    avg = serializers.IntegerField()
    min = serializers.IntegerField()
    max = serializers.IntegerField()
