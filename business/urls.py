from rest_framework import routers
from .viewset import BusinessViewset,BusinessMemberViewset

router = routers.DefaultRouter()

router.register("business",BusinessViewset,"business")
router.register("business-member",BusinessMemberViewset,"add-member")

urlpatterns = router.urls