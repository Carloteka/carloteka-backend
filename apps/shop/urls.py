from django.contrib import admin
from django.urls import path

from .views import CategoryView


urlpatterns = [
    path('categories', CategoryView.as_view(), name='categories')
]
