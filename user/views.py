from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,permissions
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer,LoginSerializer
from business.models import BusinessMember


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
    

class SetActiveBusiness(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request):
        business_id = request.data.get("business_id")

        if not business_id:
            return Response({"error":"business id is required"},status=status.HTTP_400_BAD_REQUEST)
        
        membership = BusinessMember.objects.filter(user = request.user, business = business_id).first()
        
        if not membership:
            return Response({"error":"You do not belong to this business"},status=status.HTTP_403_FORBIDDEN)
        
        request.user.active_business = membership.business
        request.user.save()

        return Response({"message":"Active business updated","active_business":{"id": membership.business.id,"name":membership.business.name,"role":membership.role}})