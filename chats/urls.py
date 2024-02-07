
from django.urls import path
from . import views

urlpatterns = [

    path('chat/<str:pk>/',views.chat,name='chat'),
    path('chat/',views.viewChat,name='inbox'),

]