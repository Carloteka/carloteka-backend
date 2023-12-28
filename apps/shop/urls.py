from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, ItemViewSet, ShopContactsViewSet, ReviewViewSet

router = DefaultRouter()
router.register(r'items', ItemViewSet, basename='item')
router.register(r'categories', CategoryViewSet, basename='category')
router.register('contacts', ShopContactsViewSet, basename='contacts')


urlpatterns = [
    path('', include(router.urls)),
    path('reviews/item/<str:item_id>/',
         ReviewViewSet.as_view({'get': 'reviews_by_item', 'post': 'add_review_by_item'}), name='reviews-by-item'),

]
