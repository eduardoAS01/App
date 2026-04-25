from rest_framework import viewsets,permissions
from .models import Business,BusinessMember
from .serializers import BusinessSerializer,BusinessMemberSerializer,ReadBusinessMemberSerializer
from rest_framework.exceptions import ValidationError,PermissionDenied
from django.contrib.auth import get_user_model

User = get_user_model()

class BusinessViewset(viewsets.ModelViewSet):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Business.objects.filter(owner = self.request.user)
    
    def perform_create(self, serializer):
        user = self.request.user

        business = serializer.save(owner = user)

        user.active_business = business
        user.save()

        BusinessMember.objects.create(
            user = user,
            business = business,
            role = "Owner"
        )

class BusinessMemberViewset(viewsets.ModelViewSet):
    queryset = BusinessMember.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    
    def get_queryset(self):
        return BusinessMember.objects.filter(business = self.request.user.active_business)
    
    
    def get_serializer_class(self):
        
        if self.action in ["list","retrieve"]:
            return ReadBusinessMemberSerializer
        
        return BusinessMemberSerializer


        

    
