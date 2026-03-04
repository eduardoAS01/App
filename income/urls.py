from rest_framework import routers
from .viewset import IncomeViewset

router = routers.DefaultRouter()

router.register("income",IncomeViewset,"income")

urlpatterns = router.urls
