from rest_framework import viewsets,permissions,filters
from .serializer import ExpenseSerializer,PurchaseSerializer
from .models import Expense,Purchase


class ExpenseViewset(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["amount","created_at"]
    ordering = ["created_at"]

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)
        

    def get_queryset(self):
        return Expense.objects.filter(user = self.request.user.active_business)

class PurchaseViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Purchase.objects.filter(user = self.request.user.active_business)