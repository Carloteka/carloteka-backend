import django_filters

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


class ReviewSelector:
    def review_list(self, filters=None):
        filters = filters or {}
        queryset = ReviewModel.objects.all()

        return ReviewFilter(filters, queryset).qs