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
        print("raw data", data)
        print("len data:", len(data))
        print("raw signature", signature)
        sign = liq_pay.str_to_sign(
            getenv("LIQPAY_PRIVATE_KEY") + data + getenv("LIQPAY_PRIVATE_KEY")
        )
        if sign != signature:
            raise NotAcceptable(detail="Signature not equal")

        response = liq_pay.decode_data_from_str(data)
        print("callback data", response)
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
            output_serializer.is_valid()
            return Response(data=output_serializer.validated_data)
        # not payed
        output_serializer = self.OutputErrorApiSerializer(data=data)
        output_serializer.is_valid()
        return Response(data=output_serializer.validated_data, status=402)

"""
order not found:
{
  "code": "payment_not_found",
  "err_code": "payment_not_found",
  "err_description": "Платеж не найден",
  "result": "error",
  "status": "error"
}
Не успішна оплата. Код помилки - limit:
{
  "result": "ok",
  "payment_id": 2432611415,
  "action": "pay",
  "status": "try_again",
  "err_code": "limit",
  "err_description": "Limit is exceeded",
  "version": 3,
  "type": "buy",
  "paytype": "card",
  "public_key": "sandbox_i55528694126",
  "acq_id": 414963,
  "order_id": "9",
  "liqpay_order_id": "VOHXV7551709408712492250",
  "description": "second",
  "sender_first_name": "sdf",
  "sender_last_name": "fsdf",
  "sender_card_mask2": "400000*02",
  "sender_card_bank": "Sandbox",
  "sender_card_type": "visa",
  "sender_card_country": 804,
  "ip": "47.62.166.91",
  "amount": 1000,
  "currency": "UAH",
  "sender_commission": 0,
  "receiver_commission": 15,
  "agent_commission": 0,
  "amount_debit": 1000,
  "amount_credit": 1000,
  "commission_debit": 0,
  "commission_credit": 15,
  "currency_debit": "UAH",
  "currency_credit": "UAH",
  "sender_bonus": 0,
  "amount_bonus": 0,
  "mpi_eci": "7",
  "is_3ds": false,
  "language": "uk",
  "create_date": 1709408712494,
  "end_date": 1709408712612,
  "transaction_id": 2432611415,
  "code": "limit"
}

Недостатньо коштів
{
  "result": "ok",
  "payment_id": 2432611415,
  "action": "pay",
  "status": "try_again",
  "err_code": "9859",
  "err_description": "Insufficient funds",
  "version": 3,
  "type": "buy",
  "paytype": "card",
  "public_key": "sandbox_i55528694126",
  "acq_id": 414963,
  "order_id": "9",
  "liqpay_order_id": "YVSEJ0JA1709409249516739",
  "description": "second",
  "sender_first_name": "fd",
  "sender_last_name": "vdfd",
  "sender_card_mask2": "400000*95",
  "sender_card_bank": "Sandbox",
  "sender_card_type": "visa",
  "sender_card_country": 804,
  "ip": "47.62.166.91",
  "amount": 1000,
  "currency": "UAH",
  "sender_commission": 0,
  "receiver_commission": 15,
  "agent_commission": 0,
  "amount_debit": 1000,
  "amount_credit": 1000,
  "commission_debit": 0,
  "commission_credit": 15,
  "currency_debit": "UAH",
  "currency_credit": "UAH",
  "sender_bonus": 0,
  "amount_bonus": 0,
  "mpi_eci": "7",
  "is_3ds": false,
  "language": "uk",
  "create_date": 1709408712494,
  "end_date": 1709409249753,
  "transaction_id": 2432611415,
  "code": "9859"
}

"""