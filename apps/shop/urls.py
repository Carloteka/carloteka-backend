from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .apis import (
    CategoryListApi,
    ShopContactsRetrieveApi,
    ItemListApi
)

categories_urlpatterns = [
    path('', CategoryListApi.as_view(), name='list'),
]

contacts_urlpatterns = [
    path('', ShopContactsRetrieveApi.as_view(), name='retrieve')
]

items_urlpatterns = [
    path('', ItemListApi.as_view(), name='list')
]

urlpatterns = [
    path('categories/', include((categories_urlpatterns, 'categories'))),
    path('contacts/', include((contacts_urlpatterns, 'contacts'))),
    path('items/', include((items_urlpatterns, 'items'))),
]
