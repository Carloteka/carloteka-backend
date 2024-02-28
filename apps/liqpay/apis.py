from django.shortcuts import render
from rest_framework.views import APIView, Response
from liqpay import LiqPay
from os import getenv


class PayApi(APIView):
    def get(self, request, *args, **kwargs):
        liqpay = LiqPay(public_key=getenv('LIQPAY_PUBLIC_KEY'), private_key=getenv('LIQPAY_PRIVATE_KEY'))
        params = {
            'action': 'pay',
            'amount': '1',
            'currency': 'UAH',
            'description': 'Payment for wooden accessories',
            'order_id': 'order_id_5',
            'version': '3',
            'sandbox': 0,
            'server_url': 'http://127.0.0.1:8000',
        }

        data = liqpay.cnb_data(params)
        signature = liqpay.cnb_signature(params)

        return Response({'data': data, 'signature': signature})


# @method_decorator(csrf_exempt, name='dispatch')
class PayCallbackApi(APIView):
    def post(self, request, *args, **kwargs):
        liqpay = LiqPay(getenv('LIQPAY_PUBLIC_KEY'), getenv('LIQPAY_PRIVATE_KEY'))
        data = request.POST.get('data')
        signature = request.POST.get('signature')
        sign = liqpay.str_to_sign(getenv('LIQPAY_PRIVATE_KEY') + data + getenv('LIQPAY_PRIVATE_KEY'))
        if sign == signature:
            print('callback is valid')
        response = liqpay.decode_data_from_str(data)
        print('callback data', response)
        return Response(200)
