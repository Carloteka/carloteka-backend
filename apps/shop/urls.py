from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, ItemViewSet, ShopContactsViewSet

router = DefaultRouter()
router.register(r'items', ItemViewSet, basename='item')
router.register(r'categories', CategoryViewSet, basename='category')
router.register('contacts', ShopContactsViewSet, basename='contacts')


urlpatterns = [
    path('', include(router.urls)),
    path('categories/<str:category_id_name>/items/<str:item_id_name>/',
         ItemViewSet.as_view({'get': 'retrieve_by_category'}), name='item-view'),

]
