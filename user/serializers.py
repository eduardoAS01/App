from user.models import User
from rest_framework import serializers

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    image = serializers.ImageField(required = False)
    
    class Meta():
        model = User
        fields = ('email','username','password','first_name','last_name','image')

    def create(self, validated_data):
        
        image = validated_data.pop('image',None)
        
        user = User.objects.create_user(**validated_data)
        
        print(user)
        if image:
            user.image = image
            user.save()
        
        return user
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only = True)