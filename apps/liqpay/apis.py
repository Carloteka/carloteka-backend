from rest_framework.views import APIView, Response
from liqpay.liqpay import LiqPay


class PayApi(APIView):
    liqpay = LiqPay()


class PayCallbackApi(APIView):
    pass
