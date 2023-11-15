from rest_framework.response import Response
from rest_framework.views import APIView

from .shop_serializers import CategorySerializer
from .models import CategoryModel


class CategoryView(APIView):
    def get(self, request):
        categories = CategoryModel.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

