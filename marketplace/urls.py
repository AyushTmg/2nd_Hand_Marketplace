
from . import views
from .views import ( 
    HomeView,
    CreateItemView,
    ItemDetailView,
    ItemDeleteView,
    ReplyView,
    CommentDeleteView,
    ReplyDeleteView
    )

from django.urls import path

urlpatterns = [


    path('',HomeView.as_view(),name='home'),
    path('create-item/',CreateItemView.as_view(),name='create-item'),
    path('item-detail/<str:pk>/',ItemDetailView.as_view(),name='item-detail'),
    path('add-reply/<str:pk>/',ReplyView.as_view(),name='add-reply'),
    path('item-delete/<str:pk>/',ItemDeleteView.as_view(),name='item-delete'),
    path('comment-delete/<str:pk>/',CommentDeleteView.as_view(),name='comment-delete'),
    path('reply-delete/<str:pk>/',ReplyDeleteView.as_view(),name='reply-delete'),
    path('item-category/<str:pk>/',views.category,name='item-category'),

]


