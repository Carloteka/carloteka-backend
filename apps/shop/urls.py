from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    ItemViewSet,
    ReviewViewSet
)
from .apis import (
    CategoryListApi,
    ShopContactsRetrieveApi,
    ItemListApi
)

router = DefaultRouter()
router.register(r'items_viewset', ItemViewSet, basename='item')

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
    path('', include(router.urls)),
    path('reviews/item/<str:item_id>/', ReviewViewSet.as_view({'get': 'reviews_by_item', 'post': 'add_review_by_item'}), name='reviews-by-item'),
    path('categories/', include((categories_urlpatterns, 'categories'))),
    path('contacts/', include((contacts_urlpatterns, 'contacts'))),
    path('items/', include((items_urlpatterns, 'items'))),
]
