from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from business.models import Business
from .models import Expense,Purchase
from inventory.models import Product
from faker import Faker

fake = Faker()
User = get_user_model()

class ExpenseTests(APITestCase):

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

        self.purchase = Purchase.objects.create(
            user = self.user,
            amount = 2000,
            business = self.business,
            )
        
        self.client.force_authenticate(user=self.user)

        self.url_expense_list = reverse("expense-list")
        self.url_expense_detail = reverse("expense-detail",args=[self.expense.id])
        self.url_purchase_list = reverse("purchase-list")
        self.url_purchase_detail = reverse("purchase-detail",args=[self.purchase.id])

    def test_create_expense(self):
        data = {
            "expense_type":"PAYMENTS",
            "comment":"This is a new comment",
            "amount": 5000,
        }

        response = self.client.post(self.url_expense_list,data,format="json")
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(Expense.objects.count(),2)
        self.assertEqual(Expense.objects.last().comment,"This is a new comment") 

    def test_create_expense_with_products(self):
        data = {
            "expense_type":"PURCHASE_PRODUCT",
            "comment":"This is a new comment",
            "products":[
                {
                    "product": self.product.id,
                    "quantity": 5
                }
            ]
        }

        response = self.client.post(self.url_expense_list,data,format="json")
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(Expense.objects.count(),2)
        self.assertEqual(Expense.objects.last().comment,"This is a new comment")


    def test_get_expense_list(self):
        response = self.client.get(self.url_expense_list)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data),1)

    def test_get_expense_detail(self):
        response = self.client.get(self.url_expense_detail)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data["comment"],"This is an old comment")

    def test_patch_expense(self):
        data = {
            "comment":"This is an updated comment",
            "amount": 3000
        }

        response = self.client.patch(self.url_expense_detail,data,format="json")
        print(response.data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(Expense.objects.count(),1)
        

    def test_delete_expense(self):
        response = self.client.delete(self.url_expense_detail)
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
        self.assertEqual(Expense.objects.count(),0)

    def test_get_purchase_list(self):
        response = self.client.get(self.url_purchase_list)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data),1)

    def test_get_purchase_detail(self):
        response = self.client.get(self.url_purchase_detail)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data["amount"],"2000.00")   