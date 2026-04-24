from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,permissions
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer,LoginSerializer



class RegisterView(APIView):
    def post(self,request):
        serializer = RegisterSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        print(user)
        return Response(
            {"message":"Succesfully register user"},
            status=status.HTTP_201_CREATED
        )
    
class LoginView(APIView):
    def post(self,request):
        serializer = LoginSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = authenticate(username = email, password = password)

        if not user:
            return Response(
                {"detail":"Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "refres":str(refresh),
                "access":str(refresh.access_token)
            },
            status=status.HTTP_200_OK
        )
    