from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    ItemViewSet,
    ShopContactsViewSet,
    ReviewViewSet
)
from .apis import (
    CategoryListApi,
)

router = DefaultRouter()
router.register(r'items', ItemViewSet, basename='item')
# router.register(r'categories', CategoryViewSet, basename='category')
router.register('contacts', ShopContactsViewSet, basename='contacts')

categories_urlpatterns = [
    path('', CategoryListApi.as_view(), name='list')
]

urlpatterns = [
    path('', include(router.urls)),
    path('reviews/item/<str:item_id>/', ReviewViewSet.as_view({'get': 'reviews_by_item', 'post': 'add_review_by_item'}), name='reviews-by-item'),
    path('categories/', include((categories_urlpatterns, 'categories')))
]
