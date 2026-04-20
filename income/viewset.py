from rest_framework import viewsets,permissions,filters
from .serializer import IncomeSerializer,SaleSerializer
from .models import Income,Sale


class IncomeViewset(viewsets.ModelViewSet):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["amount","created_at"]
    ordering = ["created_at"]

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)
        

    def get_queryset(self):
        return Income.objects.filter(user = self.request.user.active_business)
    
class SaleViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Sale.objects.filter(user = self.request.user.active_business)