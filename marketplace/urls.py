
from django.urls import path
from .views import HomeView,CreateItemView,ItemDetailView
from . import views

urlpatterns = [
    path('',HomeView.as_view(),name='home'),
    path('create-item/',CreateItemView.as_view(),name='create-item'),
    path('item-detail/<str:pk>/',ItemDetailView.as_view(),name='item-detail'),

    

]
