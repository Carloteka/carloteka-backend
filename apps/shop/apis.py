from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from .selectors import (
    CategorySelector,
    ShopContactsSelector,
)
from .models import (
    CategoryModel,
    ShopContactsModel,
    OrderModel,
    CategoryImageModel,
    ItemImageModel,
    ItemModel
)
from .serializers import (
    CategoryImageSerializer,
)


class CategoryListApi(APIView, CategorySelector):
    class OutputSerializer(serializers.ModelSerializer):
        images = CategoryImageSerializer(many=True)

        class Meta:
            ref_name = 'shop.CategoryListOutputSerializer'
            model = CategoryModel
            fields = '__all__'

    @extend_schema(
        responses={200: OutputSerializer()}
    )
    def get(self, request):
        queryset = self.category_list(params=request.query_params)
        data = self.OutputSerializer(queryset, many=True).data
        return Response(data, status=status.HTTP_200_OK)


class ShopContactsRetrieveApi(APIView, ShopContactsSelector):
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            ref_name = 'shop.ShopContactsOutputSerializer'
            model = ShopContactsModel
            fields = '__all__'

    @extend_schema(
        responses={201: OutputSerializer()}
    )
    def get(self, request):
        queryset = self.shop_contacts_retrieve_no_pk()
        data = self.OutputSerializer(queryset).data
        return Response(data, status=status.HTTP_200_OK)
