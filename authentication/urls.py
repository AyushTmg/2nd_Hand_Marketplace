from .views import UserRegistrationView,UserLoginView,UserLogoutView,ChangePasswordView
from django.urls import path

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/",UserLogoutView.as_view(),name='logout'),
    path("change-password/",ChangePasswordView.as_view(),name='change-password'),
]
