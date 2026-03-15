from rest_framework import routers
from .viewset import IncomeViewset,SaleViewset

router = routers.DefaultRouter()

router.register("income",IncomeViewset,"income")
router.register("sale",SaleViewset,"sale")

urlpatterns = router.urls
