from django.urls import path, include

from .apis import (
    CategoryListApi,
    ShopContactsRetrieveApi,
    ItemListApi,
    ItemRetrieveApi,
    ReviewListApi,
    OrderCreateAPI,
    OrderRetrieveAPI,
    ReviewCreateApi,
)
from .apis_nova_post import AreasAPI, SettlementsAPI, WarehousesAPI, CreateContactAPI, ListContactsAPI, \
    CreateWaybillAPI, PrintWaybillAPI, SetSenderAdressAPI

categories_urlpatterns = [
    path('', CategoryListApi.as_view(), name='list'),
]
contacts_urlpatterns = [
    path('', ShopContactsRetrieveApi.as_view(), name='retrieve')
]
items_urlpatterns = [
    path('', ItemListApi.as_view(), name='list'),
    path('<str:item_slug>/', ItemRetrieveApi.as_view(), name='retrieve'),
    path('<int:item_id>/reviews/', ReviewListApi.as_view(), name='list_item_reviews'),
    path('<int:item_id>/reviews/create/', ReviewCreateApi.as_view(), name='create_item_reviews'),
]
reviews_urlpatterns = [
]
orders_urlpatterns = [
    path('<int:pk>/', OrderRetrieveAPI.as_view(), name='retrieve'),
    path('create/', OrderCreateAPI.as_view(), name='create')
]
np_urlpatterns = [
    path('sender_address/', SetSenderAdressAPI.as_view(), name='sender_address'),
    path('areas/', AreasAPI.as_view(), name='areas'),
    path('settlements/', SettlementsAPI.as_view(), name='settlements'),
    path('warehouses/', WarehousesAPI.as_view(), name='warehouses'),
    path('contact/create/', CreateContactAPI.as_view(), name='create_contact'),
    path('contact/list/', ListContactsAPI.as_view(), name='list_contacts'),
    path('waybill/create/', CreateWaybillAPI.as_view(), name='create_waybill'),
    path('waybill/print/<int:waybill_number>', PrintWaybillAPI.as_view(), name='print_waybill'),
]
urlpatterns = [
    path('categories/', include((categories_urlpatterns, 'categories'))),
    path('contacts/', include((contacts_urlpatterns, 'contacts'))),
    path('items/', include((items_urlpatterns, 'items'))),
    path('reviews/', include((reviews_urlpatterns, 'reviews'))),
    path('orders/', include((orders_urlpatterns, 'orders'))),
    path('np/', include((np_urlpatterns, 'np'))),
]
