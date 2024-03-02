from django.urls import path

from .apis import PayApi, PayCallbackApi


urlpatterns = [
    path('create-liqpay-button/', PayApi.as_view(), name='pay'),
    path('pay-callback/', PayCallbackApi.as_view(), name='pay_callback'),
]
