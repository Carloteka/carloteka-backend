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
    category__id_name = django_filters.AllValuesMultipleFilter()

    class Meta:
        model = ItemModel
        fields = ('stock', 'price', 'category__id_name')


class ReviewFilter(django_filters.FilterSet):
    class Meta:
        model = ReviewModel
        fields = ['stars', 'item__id']
