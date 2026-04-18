from rest_framework import serializers
from .models import Business,BusinessMember


class BusinessSerializer(serializers.ModelSerializer):

    class Meta():
        model = Business
        fields = ("name",)


class BusinessMemberSerializer(serializers.ModelSerializer):
    email = serializers.CharField()

    class Meta():
        model = BusinessMember
        fields = ("email","role")

