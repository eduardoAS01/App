from rest_framework import routers
from .viewset import ExpenseViewset,PurchaseViewset

router = routers.DefaultRouter()

router.register("expense",ExpenseViewset,"expense")
router.register("purchase",PurchaseViewset,"purchase")

urlpatterns = router.urls