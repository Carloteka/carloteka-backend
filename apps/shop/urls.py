from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    ItemViewSet,
    ReviewViewSet
)
from .apis import (
    CategoryListApi,
    ShopContactsRetrieveApi
)

router = DefaultRouter()
router.register(r'items', ItemViewSet, basename='item')

categories_urlpatterns = [
    path('', CategoryListApi.as_view(), name='list'),
]

contacts_urlpatterns = [
    path('', ShopContactsRetrieveApi.as_view(), name='retrieve')
]

urlpatterns = [
    path('', include(router.urls)),
    path('reviews/item/<str:item_id>/', ReviewViewSet.as_view({'get': 'reviews_by_item', 'post': 'add_review_by_item'}), name='reviews-by-item'),
    path('categories/', include((categories_urlpatterns, 'categories'))),
    path('contacts/', include((contacts_urlpatterns, 'contacts'))),
]
