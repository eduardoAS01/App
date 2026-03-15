from .models import Product
from rest_framework import viewsets, permissions,filters,status
from rest_framework.response import Response
from .serializers import WriteProductSerializer,ReadProductSerializer
from .services import ProductService
from invetory_record.models import StockMovement
from django.db import transaction

class ProductViewset(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["sale_price","cost_price","quantity","profit","profit_percentage","created_at"]
    ordering = ["created_at"]

    def get_serializer_class(self):
        
        if self.action in ["list","retrieve"]:
            return ReadProductSerializer
        
        return WriteProductSerializer

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
        product = serializer.save(user = self.request.user)
        StockMovement.objects.create(
           product = product,
           new_quantity = product.quantity,
           reason = "INITIAL"
        )

    def get_queryset(self):
        return Product.objects.filter(user = self.request.user)

    def update(self, request, *args, **kwargs):
        with transaction.atomic():
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            cost_price = serializer.validated_data.get('cost_price')
            sale_price = serializer.validated_data.get('sale_price')
            validation = {"warning":False}

            if cost_price and sale_price:  
                validation  = ProductService.check_profit(cost_price,sale_price)

            self.perform_update(serializer)
            response_data = dict(serializer.data)

            if validation['warning']:
                response_data['warning'] = validation['message']

            return Response(response_data)
    
    def perform_update(self, serializer):
        with transaction.atomic():
            old_product = self.get_object()
        
            old_quantity = old_product.quantity

            updated_product = serializer.save()
        
            new_quantity = updated_product.quantity

            difference = new_quantity - old_quantity

            if difference != 0:
                StockMovement.objects.create(
                    product = updated_product,
                    new_quantity = new_quantity,
                    old_quantity = old_quantity,
                    quantity_change = difference,
                    reason = "ADJUSTMENT"
                )
