from rest_framework import routers
from django.urls import path
from .viewset import BusinessViewset,BusinessMemberViewset
from .views import SetActiveBusiness,GetBusinesses

router = routers.DefaultRouter()

router.register("business",BusinessViewset,"business")
router.register("business-member",BusinessMemberViewset,"add_member")


urlpatterns = router.urls + [
    path("business/set-active",SetActiveBusiness.as_view(),name = "set_active_business"),
    path("business/my-businesses",GetBusinesses.as_view(),name = "get_my_businesses"),
]