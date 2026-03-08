from rest_framework import viewsets,permissions,filters
from .serializer import IncomeSerializer
from .models import Income,Sale,SaleItem
from invetory_record.models import StockMovement

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
        return Income.objects.filter(user = self.request.user)
    
