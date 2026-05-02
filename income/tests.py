from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from business.models import Business
from .models import Income,Sale
from inventory.models import Product
from faker import Faker

fake = Faker()
User = get_user_model()

class IncomeTests(APITestCase):

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

        self.sale = Sale.objects.create(
            user = self.user,
            amount = 2000,
            business = self.business
        )

        self.income = Income.objects.create(
            user = self.user,
            amount = 1000,
            income_type = "LOAN",
            business = self.business,
            comment = "This is an old comment"
        )

        
        self.client.force_authenticate(user=self.user)

        self.url_income_list = reverse("income-list")
        self.url_income_detail = reverse("income-detail",args=[self.income.id])

    
    def test_create_income(self):

        data = {
            "income_type": "LOAN",
            "amount":1000
        }
        
        response = self.client.post(self.url_income_list,data)

        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

    def test_create_product_sale_income(self):

        data = {
            "income_type": "PRODUCT_SALE",
            "products":[
                {
                    "product":self.product.id,
                    "quantity":20
                }
            ]
        }
        
        response = self.client.post(self.url_income_list,data,format="json")

        self.assertEqual(response.status_code,status.HTTP_201_CREATED)        
    
    
    def test_get_incomes(self):

        response = self.client.get(self.url_income_list)

        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_get_income_detail(self):

        response = self.client.get(self.url_income_detail)

        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_patch_income(self):

        data = {
            "amount": 1500
        }

        response = self.client.patch(self.url_income_detail,data,format="json")

        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_delete_income(self):

        response = self.client.delete(self.url_income_detail)

        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
    
