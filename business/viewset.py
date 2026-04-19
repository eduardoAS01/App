from rest_framework import viewsets,permissions
from .models import Business,BusinessMember
from .serializers import BusinessSerializer,BusinessMemberSerializer
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
        
        business = serializer.save(owner = self.request.user)

        BusinessMember.objects.create(
            user = self.request.user,
            business = business,
            role = "Owner"
        )

class BusinessMemberViewset(viewsets.ModelViewSet):
    queryset = BusinessMember.objects.all()
    serializer_class = BusinessMemberSerializer
    permission_classes = [permissions.IsAuthenticated]


        

    
