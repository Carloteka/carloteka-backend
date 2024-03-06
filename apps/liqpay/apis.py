from os import getenv

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import serializers
from rest_framework.exceptions import NotAcceptable, NotFound
from rest_framework.views import APIView, Response

from apps.core.exceptions import ErrorSerializer404
from apps.liqpay.utils import change_order_payment_status
from liqpay import LiqPay

from apps.shop.servises import get_order_by_id

liq_pay = LiqPay(getenv("LIQPAY_PUBLIC_KEY"), getenv("LIQPAY_PRIVATE_KEY"))


class PayApi(APIView):
    class InputPayApiSerializer(serializers.Serializer):
        order_id = serializers.IntegerField()

    class OutputPayApiSerializer(serializers.Serializer):
        data = serializers.CharField(max_length=255)
        signature = serializers.CharField(max_length=150)

    @extend_schema(
        tags=["liqpay"],
        summary="Get params for link",
        responses={200: OutputPayApiSerializer(), 404: ErrorSerializer404()},
        parameters=[
            OpenApiParameter(
                name="order_id",
                location=OpenApiParameter.QUERY,
                description="order_id",
                required=True,
                type=int,
            ),
        ],
    )
    def get(self, request, *args, **kwargs):
        serializer = self.InputPayApiSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        order = get_order_by_id(serializer.validated_data["order_id"])
        params = {
            "action": "pay",
            "amount": str(order.total_amount),
            "currency": "UAH",
            "description": ", ".join([item.name for item in order.item_set.all()]),
            "order_id": order.id,
            "version": "3",
            "result_url": getenv("HOST_SERVER") + "/liqpay/pay-status/",
            "server_url": getenv("HOST_CLIENT") + "/api/liqpay/pay-callback/",
        }

        data = liq_pay.cnb_data(params)
        signature = liq_pay.cnb_signature(params)
        return Response({"data": data, "signature": signature})


# @method_decorator(csrf_exempt, name="dispatch")
class PayCallbackApi(APIView):

    def post(self, request, *args, **kwargs):
        data = request.data.get('data')
        signature = request.data.get('signature')
        sign = liq_pay.str_to_sign(
            getenv("LIQPAY_PRIVATE_KEY") + data + getenv("LIQPAY_PRIVATE_KEY")
        )
        if sign != signature:
            raise NotAcceptable(detail="Signature not equal")

        response = liq_pay.decode_data_from_str(data)
        # change status payment in order
        if response["status"] == "success":
            change_order_payment_status(
                response["order_id"], "liqpay", response["acq_id"]
            )
        else:
            change_order_payment_status(
                response["order_id"], "error", response["acq_id"]
            )
        return Response(200)


class GetLiqPayStatusApi(APIView):
    """Return status of liqpay payment"""

    class InputGetLiqPayStatusApi(serializers.Serializer):
        order_id = serializers.IntegerField()

    class OutputGetLiqPayStatusApi(serializers.Serializer):
        action = serializers.CharField(max_length=50)
        payment_id = serializers.IntegerField()
        status = serializers.CharField(max_length=50)  # must be success
        paytype = serializers.CharField(max_length=50)
        acq_id = serializers.IntegerField()
        sender_phone = serializers.CharField(max_length=50, required=False)
        description = serializers.CharField(max_length=250)
        amount = serializers.FloatField()

    class OutputErrorApiSerializer(serializers.Serializer):
        err_code = serializers.CharField(max_length=255, required=False)
        status = serializers.CharField(max_length=50)  # must be success
        err_description = serializers.CharField(max_length=255)

    @extend_schema(
        tags=["liqpay"],
        summary="Get status of liqpay payment",
        description="200 - the bill is paid, 402 - the bill has not been paid",
        responses={200: OutputGetLiqPayStatusApi(),
                   402: OutputErrorApiSerializer(),
                   404: ErrorSerializer404()},
        parameters=[
            OpenApiParameter(
                name="order_id",
                location=OpenApiParameter.QUERY,
                description="order_id",
                required=True,
                type=int,
            ),
        ],
    )
    def get(self, request, *args, **kwargs):
        serializer = self.InputGetLiqPayStatusApi(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        params = {
            "action": "status",
            "version": "3",
            "order_id": serializer.validated_data["order_id"],
        }
        data = liq_pay.api("request", params)
        if data["status"] == "error":
            raise NotFound(data["err_description"])

        if data["status"] == "success":
            output_serializer = self.OutputGetLiqPayStatusApi(data=data)
            output_serializer.is_valid(raise_exception=True)
            return Response(data=output_serializer.validated_data)
        # not payed
        output_serializer = self.OutputErrorApiSerializer(data=data)
        output_serializer.is_valid(raise_exception=True)
        return Response(data=output_serializer.validated_data, status=402)
