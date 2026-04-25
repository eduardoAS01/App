from rest_framework import routers
from .viewset import StockMovementViewset

router = routers.DefaultRouter()

router.register("stock-movements",StockMovementViewset,"stock_movements")

urlpatterns = router.urls