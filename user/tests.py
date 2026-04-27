from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from faker import Faker

User = get_user_model()
fake = Faker()

# Create your tests here.
class AuthTests(APITestCase):

    def test_register_user(self):
        
        url = reverse("register")
        data = {
            "username": fake.user_name(),
            "email":fake.email(),
            "first_name":fake.name(),
            "last_name":fake.last_name(),
            "password":fake.password(length=8)
        }

        response = self.client.post(url,data)

        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

    def test_login_user(self):

        url = reverse("login")

        User.objects.create_user(
            username="paco",
            email="paco@gmail.com",
            password = "qwerty1234."
        )

        data = {
            "email":"paco@gmail.com",
            "password":"qwerty1234."
        }

        response = self.client.post(url,data)

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertTrue(response.data["access"])
        self.assertTrue(response.data["refres"])
