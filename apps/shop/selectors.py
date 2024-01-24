import django_filters
from django.http import Http404

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


class ReviewSelector:
    def review_list(self, item_slug, filters=None):
        filters = filters or {}
        try:
            queryset = ItemModel.objects.get(slug=item_slug).review_set
        except ItemModel.DoesNotExist:
            raise Http404()
        return ReviewFilter(filters, queryset).qs