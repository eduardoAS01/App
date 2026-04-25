from .models import BusinessMember
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,permissions
from .serializers import ReadBusinessSerializer

class SetActiveBusiness(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request):
        business = request.data.get("business")

        if not business:
            return Response({"error":"business id is required"},status=status.HTTP_400_BAD_REQUEST)
        
        membership = BusinessMember.objects.filter(user = request.user, business = business).first()
        
        if not membership:
            return Response({"error":"You do not belong to this business"},status=status.HTTP_403_FORBIDDEN)
        
        request.user.active_business = membership.business
        request.user.save()

        return Response({"message":"Active business updated","active_business":{"id": membership.business.id,"name":membership.business.name,"role":membership.role}})
    

class GetBusinesses(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):
        user = self.request.user
        businesses = BusinessMember.objects.filter(user = user).select_related("business")
        serializer = ReadBusinessSerializer(businesses,many = True)

        return Response({
            "active_business": user.active_business.name,
            "business": serializer.data
        })
