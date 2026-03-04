from django.contrib.auth.models import User
from rest_framework import serializers

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    

    class Meta():
        model = User
        fields = ("first_name","email","password")

    def create(self, validated_data):
        user = User.objects.create_user(
            first_name= validated_data["first_name"],
            username=validated_data['email'],
            email = validated_data['email'],
            password= validated_data['password']
        )
        return user
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only = True)