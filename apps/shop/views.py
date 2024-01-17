from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import APIException, NotFound
from rest_framework.response import Response

from .models import CategoryModel, ItemModel, ShopContactsModel, ReviewModel
from .paginators import StandardResultsSetPagination
from .serializers import (CategorySerializer, ItemSerializer,
                          ReviewSerializer, ShopContactsSerializer)

class ReviewViewSet(viewsets.ViewSet):

    def reviews_by_item(self, request, item_id=None):
        """Return all comments belonging to item with given ID."""
        try:
            reviews = ItemModel.objects.get(id=item_id).get_reviews()
        except (ObjectDoesNotExist, ValueError):
            raise NotFound(detail="item not found")
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def add_review_by_item(self, request, item_id=None):
        """Add a comment for item with given ID.
        example body in POST request:
        {
            "email": "email@email.email",
            "first_name": "first_name",
            "last_name": "last_name",
            "text": "text",
            "state": "pending",
            "rate_by_stars": 2
        }
        """
        try:
            item = ItemModel.objects.get(id=item_id)
        except (ObjectDoesNotExist, ValueError):
            raise NotFound(detail="item not found")
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(item_set=item)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
