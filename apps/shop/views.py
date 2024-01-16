from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import APIException, NotFound
from rest_framework.response import Response

from .models import CategoryModel, ItemModel, ShopContactsModel, Review
from .paginators import StandardResultsSetPagination
from .serializers import (CategorySerializer, ItemSerializer,
                          ReviewSerializer, ShopContactsSerializer)


def filter_items(request, queryset):
    """
    Add to /items/ endpoint query params based on filter:

    in-stock
    out-of-stock
    backorder
    specific-order
    price
    """
    params_filtering = {}  # dict of params for apply to querystring
    add_stock: list[int] = []
    for param, value in request.query_params.items():
        match param, value:
            case "price-from", _:
                params_filtering["price__gte"] = value
            case "price-to", _:
                params_filtering["price__lte"] = value
            # in stock
            case "out-of-stock", "True":
                add_stock.append(0)
            case "in-stock", "True":
                add_stock.append(1)
            case "backorder", "True":
                add_stock.append(2)
            case "specific-order", "True":
                add_stock.append(3)
    if add_stock:
        queryset = queryset.filter(in_stock__in=add_stock)
    # Ordering
    match request.query_params.get("sort-by"):
        case "price-up":
            order_by = "price"
        case "price-down":
            order_by = "-price"
        case _:
            order_by = "name"
        # later we can add another sorting methods

    filtered_queryset = queryset.filter(**params_filtering).order_by(order_by)
    return filtered_queryset


class ItemViewSet(viewsets.ViewSet, StandardResultsSetPagination):

    def list(self, request):
        """
         Add to /items/ endpoint query parms based on filter
            limit and pagination
            Category
            in_stock = 1
            out_of_stock = 0
            backorder = 2
            specific_order = 3
        """
        categories_id_list: list[str] = request.query_params.getlist("category-id-name")

        # filtered by categories
        if categories_id_list:
            #  extract categories by ID
            categories_list: list[CategoryModel] = []
            for category_id in categories_id_list:
                try:
                    category = CategoryModel.objects.get(id_name=category_id)
                except CategoryModel.DoesNotExist:
                    raise NotFound(detail="category not found")
                categories_list.append(category)
            queryset = ItemModel.objects.filter(category__in=categories_list)
        else:
            queryset = ItemModel.objects.all()

        filtered_queryset = filter_items(request, queryset)
        results = self.paginate_queryset(filtered_queryset, request, view=self)
        serializer = ItemSerializer(results, many=True,
                                    fields=['id', 'id_name', 'name', 'mini_description', 'price', 'in_stock',
                                            'width', 'height', 'length', 'mini_image',
                                            'category__id_name', 'images'],
                                    )

        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, pk):
        item = ItemModel.objects.get(id=pk)
        serializer = ItemSerializer(item)
        return Response(serializer.data)


class ReviewViewSet(viewsets.ViewSet):

    def reviews_by_item(self, request, item_id=None):
        """Return all comments belonging to item with given ID."""
        try:
            reviews = ItemModel.objects.get(id=item_id).get_reviews()
        except (ObjectDoesNotExist, ValueError):
            raise NotFound(detail="item not found")
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def add_review_by_item(self, request, item_id=None):
        """Add a comment for item with given ID.
        example body in POST request:
        {
            "email": "email@email.email",
            "first_name": "first_name",
            "last_name": "last_name",
            "text": "text",
            "state": "pending",
            "rate_by_stars": 2
        }
        """
        try:
            item = ItemModel.objects.get(id=item_id)
        except (ObjectDoesNotExist, ValueError):
            raise NotFound(detail="item not found")
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(item_set=item)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
