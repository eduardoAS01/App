from rest_framework import serializers
from .models import Business,BusinessMember
from django.contrib.auth import get_user_model
from rest_framework.exceptions import PermissionDenied

User = get_user_model()

class BusinessSerializer(serializers.ModelSerializer):

    class Meta():
        model = Business
        fields = ("name",)


class BusinessMemberSerializer(serializers.ModelSerializer):
    email = serializers.CharField(write_only = True)

    class Meta():
        model = BusinessMember
        fields = ("email","role")

    def create(self,validated_data):
        email = validated_data.pop('email')
        user = User.objects.filter(email=email).first()
        request = self.context['request']

        membership = BusinessMember.objects.get(user = request.user)

        if not membership:
            raise serializers.ValidationError("User has no business")

        business = membership.business

        if membership.role != "Owner":
            raise PermissionDenied("Only owner can add members")
        
        if not user:
            raise serializers.ValidationError("user not found")
        
        if BusinessMember.objects.filter(user=user,business=business).exists():
            raise serializers.ValidationError("User already in business")

        validated_data['user'] = user
        validated_data['business'] = business

        return super().create(validated_data)
    
class ReadBusinessMemberSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source = "user.username", read_only = True)
    first_name = serializers.CharField(source = "user.first_name",read_only = True)
    last_name = serializers.CharField(source = "user.last_name",read_only = True)
    business_name = serializers.CharField(source = "business.name",read_only = True)

    class Meta():
        model = BusinessMember
        fields = ("username","first_name","last_name","business_name","role")
    
class ReadBusinessSerializer(serializers.ModelSerializer):
    business_name = serializers.CharField(source = "business.name",read_only = True)

    class Meta():
        model = BusinessMember
        fields = ("business_name","role")
