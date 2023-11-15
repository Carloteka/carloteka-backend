from django.contrib import admin
from django.urls import path

from .views import CategoryView, ItemView


urlpatterns = [
    path('categories',
         CategoryView.as_view(), name='categories-view'),
    path('items',
         ItemView.as_view({'get': 'list'}), name='items-view'),
    path('items/<str:pk>',
         ItemView.as_view({'get': 'retrieve'}), name='item-view'),
    path('categories/<str:category_id_name>/<str:item_id_name>',
         ItemView.as_view({'get': 'retrieve_from_category'}), name='item-view'),
]
