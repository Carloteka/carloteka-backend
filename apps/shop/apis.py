from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter
from apps.core.exceptions import (
    DEFAULT_400_EXCEPTION_DETAIL,
    DEFAULT_401_EXCEPTION_DETAIL,
    DEFAULT_403_EXCEPTION_DETAIL,
    DEFAULT_404_EXCEPTION_DETAIL,
    DEFAULT_429_EXCEPTION_DETAIL,
    ErrorSerializer404
)

from .selectors import (
    CategorySelector,
    ShopContactsSelector,
    ItemSelector,
    ReviewSelector, OrderSelector,
)
from .models import (
    OrderModel,
    ItemModel,
    ReviewModel, OrderItemModel, NovaPost
)
from .pagination import (
    get_paginated_response, LimitOffsetPagination
)
from .servises import order_create, review_create
from .utils import (
    inline_serializer
)


class CategoryListApi(APIView, CategorySelector):
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        image_set = inline_serializer(many=True, fields={
            'id': serializers.IntegerField(),
            'image': serializers.ImageField()
        })
        name = serializers.CharField()
        description = serializers.CharField()

        class Meta:
            ref_name = 'shop.CategoryListOutputSerializer'

    @extend_schema(
        responses={200: OutputSerializer()}
    )
    def get(self, request):
        queryset = self.category_list(params=request.query_params)
        data = self.OutputSerializer(queryset, many=True).data
        return Response(data, status=status.HTTP_200_OK)


class ShopContactsRetrieveApi(APIView, ShopContactsSelector):
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        work_time_mo_fr = serializers.CharField(max_length=100)
        work_time_sa = serializers.CharField(max_length=100)
        work_time_su = serializers.CharField(max_length=100)
        admin_phone = serializers.CharField(max_length=100)
        email = serializers.CharField(max_length=100)
        viber_link = serializers.CharField(max_length=100)
        telegram_link = serializers.CharField(max_length=100)

        class Meta:
            ref_name = 'shop.ShopContactsRetrieveOutputSerializer'

    @extend_schema(
        responses={200: OutputSerializer()}
    )
    def get(self, request):
        queryset = self.shop_contacts_retrieve_no_pk()
        data = self.OutputSerializer(queryset).data
        return Response(data, status=status.HTTP_200_OK)


class ItemRetrieveApi(APIView, ItemSelector):
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField(max_length=128)
        price = serializers.FloatField()
        discounted_price = serializers.FloatField(allow_null=True, required=False)
        length = serializers.FloatField(allow_null=True, required=False)
        height = serializers.FloatField(allow_null=True, required=False)
        width = serializers.FloatField(allow_null=True, required=False)
        stock = serializers.ChoiceField(choices=ItemModel.STOCK_STATUS_CHOICES)
        mini_description = serializers.CharField(max_length=2500)
        description = serializers.CharField(max_length=5000)
        image_set = inline_serializer(many=True, fields={
            'id': serializers.IntegerField(),
            'image': serializers.ImageField()
        })
        category = inline_serializer(fields={
            'id': serializers.IntegerField(),
            'name': serializers.CharField()
        })
        mini_image = serializers.ImageField(allow_null=True, required=False)
        slug = serializers.SlugField(max_length=100)
        stars = serializers.FloatField(default=0)
        review_count = serializers.IntegerField(default=0)

        class Meta:
            ref_name = 'shop.ItemRetrieveOutputSerializer'

    @extend_schema(
        tags=["Item"],
        responses={
            200: OutputSerializer(),
            404: {"detail": DEFAULT_404_EXCEPTION_DETAIL}
        },
        parameters=[
            OpenApiParameter(
                name='item_slug',
                location=OpenApiParameter.PATH,
                description='item slug',
                required=True,
                type=str
            )
        ]
    )
    def get(self, request, item_slug):
        queryset = self.item_retrieve(item_slug=item_slug)
        data = self.OutputSerializer(queryset).data
        return Response(data, status=status.HTTP_200_OK)


class ItemListApi(APIView, ItemSelector):
    class Pagination(LimitOffsetPagination):
        default_limit = 1

    class FilterSerializer(serializers.Serializer):
        stock = serializers.ListField(
            child=serializers.CharField(),
            required=False
        )
        price_max = serializers.IntegerField(required=False)
        price_min = serializers.IntegerField(required=False)

        order_by = serializers.CharField(default='price')

        category__id = serializers.ListField(
            child=serializers.IntegerField(),
            required=False
        )

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField(max_length=128)
        price = serializers.FloatField()
        discounted_price = serializers.FloatField(allow_null=True, required=False)
        length = serializers.FloatField(allow_null=True, required=False)
        height = serializers.FloatField(allow_null=True, required=False)
        width = serializers.FloatField(allow_null=True, required=False)
        stock = serializers.ChoiceField(choices=ItemModel.STOCK_STATUS_CHOICES)
        mini_description = serializers.CharField(max_length=2500)
        image_set = inline_serializer(many=True, fields={
            'id': serializers.IntegerField(),
            'image': serializers.ImageField()
        })
        category = inline_serializer(fields={
            'id': serializers.IntegerField()
        })
        mini_image = serializers.ImageField(allow_null=True, required=False)
        slug = serializers.SlugField(max_length=100)
        stars = serializers.FloatField(default=0)
        review_count = serializers.IntegerField(default=0)

        class Meta:
            ref_name = 'shop.ItemListOutputSerializer'

    @extend_schema(
        tags=["Item"],
        responses={200: OutputSerializer()},
        parameters=[
            OpenApiParameter(
                name='category__id',
                location=OpenApiParameter.QUERY,
                description='category id',
                required=False,
                type=int,
                many=True
            ),
            OpenApiParameter(
                name='stock',
                location=OpenApiParameter.QUERY,
                description='stock state of item (you can select more then one by holding control button',
                required=False,
                type=str,
                many=True,
                enum=('IN_STOCK', 'OUT_OF_STOCK', 'BACKORDER', 'SPECIFIC_ORDER')
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


class ReviewListApi(APIView, ReviewSelector):
    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class FilterSerializer(serializers.Serializer):
        order_by = serializers.CharField(default='stars')

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            ref_name = 'shop.ReviewOutputSerializer'
            model = ReviewModel
            fields = '__all__'

    @extend_schema(
        tags=["Review"],
        responses={200: OutputSerializer(),
                   404: ErrorSerializer404()
                   },
        parameters=[
            OpenApiParameter(
                name='order_by',
                location=OpenApiParameter.QUERY,
                description='order by stars or date',
                required=False,
                type=str,
                enum=('stars', '-stars', "date", "-date")
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
            )
        ],
    )
    def get(self, request, item_id):
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)
        reviews = self.review_list(filters=filters_serializer.validated_data, item_id=item_id)

        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=reviews,
            request=request,
            view=self
        )


class ReviewCreateApi(APIView):
    class InputReviewCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = ReviewModel
            fields = (
                "email",
                "first_name",
                "last_name",
                "text",
                "stars"
            )

    @extend_schema(
        tags=["Review"],
        summary="Create a review",
        request=InputReviewCreateSerializer,
        responses={201: status.HTTP_201_CREATED,
                   404: ErrorSerializer404(),
                   },
    )
    def post(self, request, item_id):
        serializer = self.InputReviewCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reviews = review_create(item_id=item_id, **serializer.validated_data)

        return Response(status=status.HTTP_201_CREATED, data={"review_id": reviews.id})


class OrderCreateAPI(APIView):
    class InputOrdersSerializer(serializers.ModelSerializer):
        items = inline_serializer(
            name="items",
            many=True,
            fields={
                "quantity": serializers.IntegerField(),
                "item": serializers.IntegerField(),
            },
        )
        waybill_np = inline_serializer(
            name="waybill_np",
            many=False,
            required=False,
            fields={
                "ref": serializers.UUIDField(),
                "int_doc_number": serializers.IntegerField(),
                "cost_on_site": serializers.IntegerField(),
                "estimated_delivery_date": serializers.DateField()
            }
        )

        class Meta:
            model = OrderModel
            exclude = ["item_set", "nova_post"]

    @extend_schema(
        tags=["Order"],
        request=InputOrdersSerializer,
        responses={
            201: status.HTTP_201_CREATED,
            404: ErrorSerializer404(),
        },
    )
    def post(self, request):
        """Create a new order."""
        serializer = self.InputOrdersSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = order_create(**serializer.validated_data)
        return Response(status=status.HTTP_201_CREATED, data={"order_id": order.id})


class OrderRetrieveAPI(APIView, OrderSelector):
    class OrdersSerializer(serializers.ModelSerializer):
        item_set = serializers.SerializerMethodField()
        nova_post = serializers.SerializerMethodField()

        class Meta:
            model = OrderModel
            fields = "__all__"

        class OrderItemsSerializer(serializers.ModelSerializer):
            class Meta:
                model = OrderItemModel
                exclude = ["id", "order"]

        def get_item_set(self, obj) -> dict:
            items = obj.get_items()
            serializer = self.OrderItemsSerializer(items, many=True)
            return serializer.data

        class NovaPostSerializer(serializers.ModelSerializer):
            class Meta:
                model = NovaPost
                fields = "__all__"

        def get_nova_post(self, obj) -> dict:
            nova_post = obj.nova_post
            serializer = self.NovaPostSerializer(nova_post)
            return serializer.data

    class OutputOrdersSerializer(serializers.ModelSerializer):
        """For swagger represents."""
        class Meta:
            model = OrderModel
            fields = "__all__"

        nova_post = inline_serializer(
            name="waybill_np_retrieve",
            many=False,
            required=False,
            fields={
                "ref": serializers.UUIDField(),
                "int_doc_number": serializers.IntegerField(),
                "cost_on_site": serializers.IntegerField(),
                "estimated_delivery_date": serializers.DateField()
            }
        )

        items = inline_serializer(
            name="items_retrieve",
            many=True,
            fields={
                "quantity": serializers.IntegerField(),
                "item": serializers.IntegerField(),
            },
        )

    @extend_schema(
        tags=["Order"],
        responses={
            200: OutputOrdersSerializer,
            404: ErrorSerializer404(),
        },
    )
    def get(self, request, pk):
        """Retrieve an order."""
        order = self.get_order_by_id(pk)
        serializer = self.OrdersSerializer(order, many=False)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
