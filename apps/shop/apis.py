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
from .pagination import (
    get_paginated_response, LimitOffsetPagination
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
    class Pagination(LimitOffsetPagination):
        default_limit = 1

    class FilterSerializer(serializers.Serializer):
        in_stock = serializers.ListField(
            child=serializers.IntegerField(),
            required=False
        )
        price_max = serializers.IntegerField(required=False)
        price_min = serializers.IntegerField(required=False)

        order_by = serializers.CharField(default='price')

        category__id_name = serializers.ListField(
            child=serializers.CharField(),
            required=False
        )

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
                name='category__id_name',
                location=OpenApiParameter.QUERY,
                description='category id name',
                required=False,
                type=str,
                many=True
            ),
            OpenApiParameter(
                name='in_stock',
                location=OpenApiParameter.QUERY,
                description='stock state of item',
                required=False,
                type=int,
                many=True
            ),
            OpenApiParameter(
                name='price_min',
                location=OpenApiParameter.QUERY,
                description='minimal price',
                required=False,
                type=int,
                many=False
            ),
            OpenApiParameter(
                name='price_max',
                location=OpenApiParameter.QUERY,
                description='max price',
                required=False,
                type=int,
                many=False
            ),
            OpenApiParameter(
                name='order_by',
                location=OpenApiParameter.QUERY,
                description='order by something',
                required=False,
                type=str,
                enum=('price', '-price')
            ),
            OpenApiParameter(
                name='limit',
                location=OpenApiParameter.QUERY,
                description='how many objects you get',
                required=False,
                type=int
            ),
            OpenApiParameter(
                name='offset',
                location=OpenApiParameter.QUERY,
                description='page of objects',
                required=False,
                type=int
            ),
        ],
    )
    def get(self, request):
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)
        print(filters_serializer.validated_data)
        items = self.item_list(filters=filters_serializer.validated_data)

        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=items,
            request=request,
            view=self
        )
