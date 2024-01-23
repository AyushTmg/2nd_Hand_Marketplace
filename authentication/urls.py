from django.urls import path
from .views import( 
    UserRegistrationView,
    UserLoginView,
    UserLogoutView,
    ChangePasswordView,
    SendResetPasswordEmailView,
    PasswordResetView,
    UserProfileView,
    UpdateProfileView
    )



urlpatterns = [

    path("register/", UserRegistrationView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/",UserLogoutView.as_view(),name='logout'),
    path("change-password/",ChangePasswordView.as_view(),name='change-password'),
    path('send-reset-password-email/',SendResetPasswordEmailView.as_view(),name='send-reset-password-email'),
    path('reset-password/<str:uid>/<str:token>/',PasswordResetView.as_view(),name='reset-password'),
    path('user/<str:username>/',UserProfileView.as_view(),name='user-profile'),
    path('edit-profile/',UpdateProfileView.as_view(),name='edit-profile'),

]
