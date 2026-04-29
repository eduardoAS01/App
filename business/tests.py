from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from .models import Business,BusinessMember
from django.contrib.auth import get_user_model
from faker import Faker

fake = Faker()
User = get_user_model()

class BusinessTests(APITestCase):
    
    def setUp(self):
        

        self.user = User.objects.create_user(
            username="paco",
            email="paco@gmail.com",
            password = "qwerty1234.",
        )

        self.client.force_authenticate(user=self.user)

        self.business = Business.objects.create(
            name = fake.company(),
            owner = self.user
        )

        self.user.active_business = self.business

        self.business_member = BusinessMember.objects.create(
            user = self.user,
            business = self.business,
            role = "employee"
        )

        self.url_list = reverse("business-list")
        self.url_detail = reverse("business-detail",args=[self.business.id])

    def test_create_business(self):
        
        data = {
            "name": fake.company(),
            "owner": self.user
        }

        response = self.client.post(self.url_list,data)

        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

    def test_get_businesses(self):
        
        response = self.client.get(self.url_list)

        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_get_business(self):
        id = 1
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_patch_business(self):
        response = self.client.patch(self.url_detail)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_delete_business(self):
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)

    def test_set_active_business_view(self):
        url = reverse("set_active_business")

        data = {
            "business":self.business.id
        }
        response = self.client.post(url,data)

        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_my_business_view(self):
        url = reverse("get_my_businesses")
        response = self.client.get(url)

        self.assertEqual(response.status_code,status.HTTP_200_OK)