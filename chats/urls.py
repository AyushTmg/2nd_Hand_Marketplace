
from django.urls import path
from . import views

urlpatterns = [

    path('chat/<str:pk>/',views.chat,name='chat'),
    path('inbox/',views.viewChat,name='inbox'),

]