from os import getenv

from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import serializers
from rest_framework.exceptions import NotAcceptable
from rest_framework.views import APIView, Response

from apps.core.exceptions import ErrorSerializer404
from apps.liqpay.utils import change_order_payment_status
from liqpay import LiqPay

liq_pay = LiqPay(getenv("LIQPAY_PUBLIC_KEY"), getenv("LIQPAY_PRIVATE_KEY"))


class PayApi(APIView):
    class InputPayApiSerializer(serializers.Serializer):
        amount = serializers.DecimalField(max_digits=50, decimal_places=2)
        description = serializers.CharField(max_length=255)
        order_id = serializers.IntegerField()

    class OutputPayApiSerializer(serializers.Serializer):
        data = serializers.CharField(max_length=255)
        signature = serializers.CharField(max_length=150)

    @extend_schema(
        tags=["liqpay"],
        responses={200: OutputPayApiSerializer(), 404: ErrorSerializer404()},
        parameters=[
            OpenApiParameter(
                name="amount",
                location=OpenApiParameter.QUERY,
                description="amount",
                required=True,
                type=float,
            ),
            OpenApiParameter(
                name="order_id",
                location=OpenApiParameter.QUERY,
                description="order_id",
                required=True,
                type=int,
            ),
            OpenApiParameter(
                name="description",
                location=OpenApiParameter.QUERY,
                description="description",
                required=True,
                type=str,
            ),
        ],
    )
    def get(self, request, *args, **kwargs):
        serializer = self.InputPayApiSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        params = {
            "action": "pay",
            "amount": str(serializer.validated_data["amount"]),
            "currency": "UAH",
            "description": serializer.validated_data["description"],
            "order_id": serializer.validated_data["order_id"],
            "version": "3",
            "result_url": getenv("HOST_SERVER") + "/liqpay/pay-status/",
            "server_url": getenv("HOST_CLIENT") + "/api/liqpay/pay-callback/",
        }

        data = liq_pay.cnb_data(params)
        signature = liq_pay.cnb_signature(params)
        return Response({"data": data, "signature": signature})
        # return render(request,"test_liqpay_button.html", {"data": data, "signature": signature})


@method_decorator(csrf_exempt, name="dispatch")
class PayCallbackApi(APIView):
    class InputPayCallbackApiSerializer(serializers.Serializer):
        data = serializers.CharField(max_length=255)
        signature = serializers.CharField(max_length=255)

    def post(self, request, *args, **kwargs):
        serializer = self.InputPayCallbackApiSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data.get("data")
        signature = serializer.validated_data.get("signature")

        sign = liq_pay.str_to_sign(
            getenv("LIQPAY_PRIVATE_KEY") + data + getenv("LIQPAY_PRIVATE_KEY")
        )
        if sign != signature:
            raise NotAcceptable(detail="Signature not equal")

        response = liq_pay.decode_data_from_str(data)
        print("callback data", response)
        # change status payment in order
        if response.status == "success":
            change_order_payment_status(
                response["order_id"], "liqpay", response["acq_id"]
            )
        else:
            change_order_payment_status(
                response["order_id"], "error", response["acq_id"]
            )
        return Response(200)
