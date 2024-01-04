from .views import UserRegistrationView,UserLoginView,UserLogoutView,ChangePasswordView,SendResetPasswordEmailView,PasswordResetView
from django.urls import path

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/",UserLogoutView.as_view(),name='logout'),
    path("change-password/",ChangePasswordView.as_view(),name='change-password'),
    path('send-reset-password-email/',SendResetPasswordEmailView.as_view(),name='send-reset-password-email'),
    path('reset-password/<str:uid>/<str:token>/',PasswordResetView.as_view(),name='reset-password'),
]
