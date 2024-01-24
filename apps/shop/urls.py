from django.urls import path, include

from .apis import (
    CategoryListApi,
    ShopContactsRetrieveApi,
    ItemListApi,
    ItemRetrieveApi,
    ReviewListApi,
)

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

urlpatterns = [
    path('categories/', include((categories_urlpatterns, 'categories'))),
    path('contacts/', include((contacts_urlpatterns, 'contacts'))),
    path('items/', include((items_urlpatterns, 'items'))),
    path('reviews/', include((reviews_urlpatterns, 'reviews'))),
]
