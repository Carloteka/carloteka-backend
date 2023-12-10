from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, permissions
from rest_framework.exceptions import APIException

from .shop_serializers import CategorySerializer, ItemSerializer, ShopContactsSerializer, OrderSerializer
from .models import CategoryModel, ItemModel, ShopContactsModel, OrderModel


class CategoryViewSet(viewsets.ViewSet):
    def list(self, request):
        categories = CategoryModel.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class ItemViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = ItemModel.objects.all()
        serializer = ItemSerializer(queryset, many=True, fields=['id', 'id_name', 'name', 'mini_description', 'price',
                                                              'width', 'height', 'length', 'mini_image',
                                                              'category__id_name', 'images'])
        return Response(serializer.data)

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


class OrderViewSet(viewsets.ModelViewSet):
    queryset = OrderModel.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAdminUser]