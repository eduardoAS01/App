from .models import StockMovement
from rest_framework import viewsets,permissions
from .serializers import StockMovementSerializer


class StockMovementViewset(viewsets.ReadOnlyModelViewSet):
    queryset = StockMovement.objects.all()
    serializer_class = StockMovementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return StockMovement.objects.filter(business = self.request.user.active_business)