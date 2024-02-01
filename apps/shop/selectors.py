import django_filters
from rest_framework import exceptions

from .models import (
    CategoryModel,
    ShopContactsModel,
    ItemModel,
    ItemImageModel,
    OrderModel,
    ReviewModel
)
from .filters import (
    ItemFilter,
    ReviewFilter
)


class CategorySelector:
    def category_list(self, params=None):
        queryset = CategoryModel.objects.all()
        return queryset


class ShopContactsSelector:
    def shop_contacts_retrieve_no_pk(self):
        queryset = ShopContactsModel.objects.first()
        return queryset


class ItemSelector:
    def item_list(self, filters=None):
        filters = filters or {}
        queryset = ItemModel.objects.all()

        return ItemFilter(filters, queryset).qs

    def item_retrieve(self, item_slug):
        # TODO if object is visible - send; else - throw error 404 (in theory 403,
        #  but user should not know that we have it)
        queryset = ItemModel.objects.get(slug=item_slug)
        print(queryset)

        return queryset

    def item_retrieve_by_id(self, item_id: int) -> ItemModel:
        # TODO if object is visible - send; else - throw error 404 (in theory 403,
        #  but user should not know that we have it)
        try:
            return ItemModel.objects.get(pk=item_id)
        except ItemModel.DoesNotExist:
            raise exceptions.ValidationError({"detail": "Item not found"})


class ReviewSelector:
    def review_list(self, item_id, filters=None):
        filters = filters or {}
        try:
            queryset = ItemModel.objects.get(pk=item_id).review_set
        except ItemModel.DoesNotExist:
            raise exceptions.ValidationError({"detail": "Item not found"})
        return ReviewFilter(filters, queryset).qs

class OrderSelector:
    def get_order_by_id(self, order_id: int) -> OrderModel:
        try:
            return OrderModel.objects.get(pk=order_id)
        except OrderModel.DoesNotExist:
            raise exceptions.ValidationError({"detail": "Order not found"})
