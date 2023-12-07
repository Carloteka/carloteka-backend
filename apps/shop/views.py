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
    Add to /items/ endpoint query parms based on filter:

    State (в наявності/під замовлення)
    Size
    price
    """
    params_filtering = {}  # dict of paramt for apply to querystring
    for param, value in request.query_params.items():
        match param, value:
            case "price_from", _:
                params_filtering["price__gte"] = value
            case "price_to", _:
                params_filtering["price__lte"] = value

            case "state", "True":
                params_filtering["in_stock__gt"] = 0
            case "state", "False":
                params_filtering["in_stock"] = 0

            case "size", "big":
                params_filtering["length__gt"] = 30
                params_filtering["height__gt"] = 30
                params_filtering["width__gt"] = 30
            case "size", "small":
                params_filtering["length__lt"] = 10
                params_filtering["height__lt"] = 10
                params_filtering["width__lt"] = 10
            case "size", "medium":
                params_filtering["length__lt"] = 30
                params_filtering["height__lt"] = 30
                params_filtering["width__lt"] = 30
                params_filtering["length__gt"] = 10
                params_filtering["height__gt"] = 10
                params_filtering["width__gt"] = 10

    filtered_queryset = queryset.filter(**params_filtering)
    return filtered_queryset


class ItemViewSet(viewsets.ViewSet, StandardResultsSetPagination):

    def list(self, request):
        """
         Add to /items/ endpoint query parms based on filter
            limit and pagination
            Category
            State (в наявності/під замовлення)
            Size
        """
        if request.query_params.get("category_id_name"):
            try:
                category = CategoryModel.objects.get(id_name=request.query_params.get("category_id_name"))
            except CategoryModel.DoesNotExist:
                raise NotFound(detail="category not found")
            queryset = ItemModel.objects.filter(category=category)
        else:
            queryset = ItemModel.objects.all()
        filtered_queryset = filter_items(request, queryset)
        results = self.paginate_queryset(filtered_queryset, request, view=self)
        serializer = ItemSerializer(results, many=True,
                                    fields=['id', 'id_name', 'name', 'mini_description', 'price',
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
