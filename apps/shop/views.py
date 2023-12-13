from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.exceptions import APIException, NotFound

from .paginators import StandardResultsSetPagination
from .shop_serializers import CategorySerializer, ItemSerializer, ShopContactsSerializer
from .models import CategoryModel, ItemModel, ShopContactsModel


class CategoryViewSet(viewsets.ViewSet):
    def list(self, request):
        categories = CategoryModel.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


def filter_items(request, queryset):
    """
    Add to /items/ endpoint query params based on filter:

    in_stock
    out_of_stock
    backorder
    specific_order
    price
    """
    params_filtering = {}  # dict of params for apply to querystring
    add_stock: list[int] = []
    for param, value in request.query_params.items():
        match param, value:
            case "price_from", _:
                params_filtering["price__gte"] = value
            case "price_to", _:
                params_filtering["price__lte"] = value
            # in stock
            case "out_of_stock", "True":
                add_stock.append(0)
            case "in_stock", "True":
                add_stock.append(1)
            case "backorder", "True":
                add_stock.append(2)
            case "specific_order", "True":
                add_stock.append(3)
    if add_stock:
        queryset = queryset.filter(in_stock__in=add_stock)
    filtered_queryset = queryset.filter(**params_filtering)
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
        categories_id_list: list[str] = request.query_params.getlist("category_id_name")

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
                                    context={"request": request})

        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=['get'], url_path='categories/(?P<category_id_name>[^/.]+)/(?P<item_id_name>[^/.]+)')
    def retrieve_by_category(self, request, category_id_name=None, item_id_name=None):
        try:
            item = CategoryModel.objects.get(id_name=category_id_name).item_set.get(id_name=item_id_name)
        except ObjectDoesNotExist:
            APIException.status_code = 404
            APIException.default_detail = 'Object Not found'
            raise APIException
        serializer = ItemSerializer(item)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        item = ItemModel.objects.get(id=pk)
        serializer = ItemSerializer(item)
        return Response(serializer.data)


class ShopContactsViewSet(viewsets.ViewSet):
    def list(self, request):
        try:
            queryset = ShopContactsModel.objects.all().first()
        except ObjectDoesNotExist:
            APIException.status_code = 404
            APIException.default_detail = 'Object Not found'
            raise APIException
        serializer = ShopContactsSerializer(queryset)
        return Response(serializer.data)
