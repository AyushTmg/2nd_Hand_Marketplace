
from django.urls import path
from .views import HomeView,CreateItemView
from . import views

urlpatterns = [
    path('',HomeView.as_view(),name='home'),
    path('create-item/',CreateItemView.as_view(),name='create-item'),
    

]
