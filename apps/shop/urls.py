from django.urls import path, include

from .apis import (
    CategoryListApi,
    ShopContactsRetrieveApi,
    ItemListApi,
    ItemRetrieveApi,
    ReviewListApi,
    OrderCreateAPI,
    OrderRetrieveAPI,
)
from .apis_nova_post import AreasAPI, SettlementsAPI, WarehousesAPI

categories_urlpatterns = [
    path('', CategoryListApi.as_view(), name='list'),
]
contacts_urlpatterns = [
    path('', ShopContactsRetrieveApi.as_view(), name='retrieve')
]
items_urlpatterns = [
    path('', ItemListApi.as_view(), name='list'),
    path('<str:item_slug>/', ItemRetrieveApi.as_view(), name='retrieve'),
    path('<int:item_id>/reviews/', ReviewListApi.as_view(), name='list_item_reviews')
]
reviews_urlpatterns = [
]
orders_urlpatterns = [
    path('<int:pk>/', OrderRetrieveAPI.as_view(), name='retrieve'),
    path('create/', OrderCreateAPI.as_view(), name='create')
]
np_urlpatterns = [
    path('areas/', AreasAPI.as_view(), name='areas'),
    path('settlements/', SettlementsAPI.as_view(), name='settlements'),
    path('warehouses/', WarehousesAPI.as_view(), name='warehouses'),
]
urlpatterns = [
    path('categories/', include((categories_urlpatterns, 'categories'))),
    path('contacts/', include((contacts_urlpatterns, 'contacts'))),
    path('items/', include((items_urlpatterns, 'items'))),
    path('reviews/', include((reviews_urlpatterns, 'reviews'))),
    path('orders/', include((orders_urlpatterns, 'orders'))),
    path('np/', include((np_urlpatterns, 'np'))),
]
