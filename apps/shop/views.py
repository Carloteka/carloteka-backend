from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets

from .shop_serializers import CategorySerializer, ItemSerializer
from .models import CategoryModel, ItemModel


class CategoryView(APIView):
    def get(self, request):
        categories = CategoryModel.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class ItemView(viewsets.ViewSet):

    def list(self, request):
        items = ItemModel.objects.all()
        serializer = ItemSerializer(items, many=True, fields=['id', 'id_name', 'name', 'mini_description', 'price',
                                                              'width', 'height', 'length', 'mini_image',
                                                              'category__id_name', 'images'])
        return Response(serializer.data)

    def retrieve_from_category(self, request, category_id_name, item_id_name):
        item = CategoryModel.objects.get(id_name=category_id_name).item_set.get(id_name=item_id_name)
        serializer = ItemSerializer(item)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        item = ItemModel.objects.get(id=pk)
        serializer = ItemSerializer(item)
        return Response(serializer.data)
