from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter

from .selectors import (
    CategorySelector,
    ShopContactsSelector,
    ItemSelector,
)
from .models import (
    CategoryModel,
    ShopContactsModel,
    OrderModel,
    CategoryImageModel,
    ItemModel,
    ItemImageModel,
    ReviewModel
)
from .serializers import (
    CategoryImageSerializer,
    ItemImageSerializer,
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
            ref_name = 'shop.ShopContactsRetrieveOutputSerializer'
            model = ShopContactsModel
            fields = '__all__'

    @extend_schema(
        responses={200: OutputSerializer()}
    )
    def get(self, request):
        queryset = self.shop_contacts_retrieve_no_pk()
        data = self.OutputSerializer(queryset).data
        return Response(data, status=status.HTTP_200_OK)


class ItemListApi(APIView, ItemSelector):
    class OutputSerializer(serializers.ModelSerializer):
        images = ItemImageSerializer(many=True)

        class Meta:
            ref_name = 'shop.ItemListOutputSerializer'
            model = ItemModel
            fields = '__all__'

    @extend_schema(
        responses={200: OutputSerializer()},
        parameters=[
            OpenApiParameter(
                name='page_size',
                location=OpenApiParameter.QUERY,
                description='page size',
                required=False,
                type=int
            ),
            OpenApiParameter(
                name='page',
                location=OpenApiParameter.QUERY,
                description='page number',
                required=False,
                type=int
            ),
        ],
    )
    def get(self, request):
        queryset = self.item_list(params=request.query_params)
        data = self.OutputSerializer(queryset, many=True).data
        return Response(data={'results': data}, status=status.HTTP_200_OK)  # TODO remove 'results' while adding filters
