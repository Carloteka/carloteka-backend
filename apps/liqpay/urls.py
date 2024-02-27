from django.conf.urls import url

from .apis import PayApi, PayCallbackApi


urlpatterns = [
    url(r'^pay/$', PayApi.as_view(), name='pay_view'),
    url(r'^pay-callback/$', PayCallbackApi.as_view(), name='pay_callback'),
]