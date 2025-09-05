from rest_framework import serializers
from namer.models import *

class ComputerGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComputerGroup
        # fields = '__all__'
        fields = ["id", "name", "prefix", "divider", "domain"]


class NetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Network
        fields = '__all__'


class ComputerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Computer
        fields = '__all__'
