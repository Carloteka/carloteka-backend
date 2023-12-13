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
        category_id_name = request.query_params.get("category_id_name")
        price_from = request.query_params.get("price_from")
        price_to = request.query_params.get("price_to")
        in_stock = request.query_params.get("in_stock")
        out_of_stock = request.query_params.get("out_of_stock")
        backorder = request.query_params.get("backorder")
        specific_order = request.query_params.get("specific_order")
        # filtered by category
        if category_id_name:
            try:
                category = CategoryModel.objects.get(id_name=request.query_params.get("category_id_name"))
            except CategoryModel.DoesNotExist:
                raise NotFound(detail="category not found")
            queryset = ItemModel.objects.filter(category=category)
        else:
            queryset = ItemModel.objects.all()
        # filtered by price
        if price_from:
            queryset = queryset.filter(price__gte=price_from)
        if price_to:
            queryset = queryset.filter(price__lte=price_to)
        # filtered by stock
        add_stock = []
        if out_of_stock:
            if out_of_stock == "True":
                add_stock.append(0)
        if in_stock:
            if in_stock == "True":
                add_stock.append(1)
        if backorder:
            if backorder == "True":
                add_stock.append(2)
        if specific_order:
            if specific_order == "True":
                add_stock.append(3)
        if add_stock:
            queryset = queryset.filter(in_stock__in=add_stock)

        results = self.paginate_queryset(queryset, request, view=self)
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
