from rest_framework import routers
from .viewset import ProductViewset

router = routers.DefaultRouter()

router.register("products",ProductViewset,"products")

urlpatterns = router.urls