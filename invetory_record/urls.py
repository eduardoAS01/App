from rest_framework import routers
from .viewset import StockMovementViewset

router = routers.DefaultRouter()

router.register("stock_movements",StockMovementViewset,"stock_movements")

urlpatterns = router.urls