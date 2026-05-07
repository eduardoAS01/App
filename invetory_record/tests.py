from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from business.models import Business
from .models import StockMovement
from expense.models import Expense
from inventory.models import Product
from faker import Faker

fake = Faker()
User = get_user_model()

class InventoryRecordTests(APITestCase):

    def setUp(self):
        
        self.user = User.objects.create_user(
            username= fake.user_name(),
            email= fake.email(),
            password= fake.password()
        )

        self.business = Business.objects.create(
            name = fake.company(),
            owner = self.user
        )

        self.user.active_business = self.business

        self.product = Product.objects.create(
            name = "papa",
            cost_price = 100,
            sale_price = 200,
            quantity = 45,
            business = self.business,
            user = self.user
        )

        self.expense = Expense.objects.create(
            user = self.user,
            amount = 1000,
            expense_type = "RENT",
            business = self.business,
            comment = "This is an old comment"
        )

        self.stock_movement = StockMovement.objects.create(
            product = self.product,
            new_quantity = 50,
            old_quantity = 45,
            quantity_change = 5,
            business = self.business,
            comment = "This is an old comment"
        )
        
        self.client.force_authenticate(user=self.user)

        self.url_stock_movement_list = reverse("stock_movements-list")
        self.url_stock_movement_detail = reverse("stock_movements-detail",args=[self.stock_movement.id])


    def test_get_stock_movements(self):
        response = self.client.get(self.url_stock_movement_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_stock_movement_detail(self):
        response = self.client.get(self.url_stock_movement_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        