from django.urls import path
from .views import RegisterView,LoginView,SetActiveBusiness

urlpatterns = [
    path("register/",RegisterView.as_view(),name="register"),
    path("login/",LoginView.as_view(),name="login"),
    path("set-active-business/",SetActiveBusiness.as_view(),name="set-active-business")
]
