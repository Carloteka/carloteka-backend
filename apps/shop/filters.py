import django_filters

from .models import ItemModel


class ItemFilter(django_filters.FilterSet):
    in_stock = django_filters.AllValuesMultipleFilter()
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
        fields = ('in_stock', 'price', 'category__id_name')
