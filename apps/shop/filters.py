import django_filters

from .models import (
    ItemModel,
    ReviewModel
)


class ItemFilter(django_filters.FilterSet):
    stock = django_filters.AllValuesMultipleFilter()
    price = django_filters.RangeFilter()
    order_by = django_filters.OrderingFilter(
        # tuple mapping, ('model field name', 'parameter name')
        fields=(
            ('price', 'price')
        )
    )
    category__id = django_filters.AllValuesMultipleFilter()

    class Meta:
        model = ItemModel
        fields = ('stock', 'price', 'category__id')


class ReviewFilter(django_filters.FilterSet):
    order_by = django_filters.OrderingFilter(
        # tuple mapping, ('model field name', 'parameter name')
        fields=(
            ('stars', 'stars')
        )
    )
    class Meta:
        model = ReviewModel
        fields = ['item_id']
