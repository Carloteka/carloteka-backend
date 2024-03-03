from django.urls import path

from .apis import PayApi, PayCallbackApi, GetLiqPayStatusApi


urlpatterns = [
    path('create-liqpay-button/', PayApi.as_view(), name='pay'),
    path('pay-callback/', PayCallbackApi.as_view(), name='pay_callback'),
    path('get-status/', GetLiqPayStatusApi.as_view(), name='get_status'),
]
