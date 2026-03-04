from .models import Product
from rest_framework import viewsets, permissions,filters,status
from rest_framework.response import Response
from .serializers import ProductSerializer
from .services import ProductService

class ProductViewset(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["sale_price","cost_price","quantity","profit","profit_percentage","created_at"]
    ordering = ["created_at"]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validation = ProductService.check_profit(
            serializer.validated_data['cost_price'],
            serializer.validated_data['sale_price']
        )

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response_data = dict(serializer.data)

        if validation['warning']:
            response_data['warning'] = validation['message']

        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

    def get_queryset(self):
        return Product.objects.filter(user = self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        validation  = ProductService.check_profit(
            serializer.validated_data['cost_price'],
            serializer.validated_data['sale_price']
        )

        self.perform_update(serializer)
        response_data = dict(serializer.data)

        if validation['warning']:
            response_data['warning'] = validation['message']

        return Response(response_data)

