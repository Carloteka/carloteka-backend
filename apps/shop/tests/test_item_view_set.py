import os

import pytest
from django.conf import settings
from django.core.files import File
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.shop.models import CategoryModel, ItemModel


class TestReview:
    @pytest.fixture()
    def initialize_task_db(self):
        item_image_filename = "apps/shop/management/img/img_data.png"
        item_image_path = os.path.join(settings.BASE_DIR, item_image_filename)
        category1 = CategoryModel.objects.create(
            id_name="id_name1", name="name1", description="description1"
        )
        item1 = ItemModel(
            id_name="1",
            name="name1",
            price=12,
            mini_description="mini_description",
            description="description",
            category=category1,
        )

        if os.path.exists(item_image_path):
            with open(item_image_path, "rb") as image_file:
                django_file = File(image_file)
                item1.mini_image.save(f"mini_image_1.png", django_file, save=False)

        item1.save()

        return {"category1": category1, "item1": item1}

    @pytest.mark.django_db
    def test_item_review_get(self, initialize_task_db):
        item1 = initialize_task_db["item1"]
        url = reverse("reviews-by-item", kwargs={"item_id": item1.id})

        # test that in item1 no reviews
        client = APIClient()
        response = client.get(url)
        assert (
                response.status_code == status.HTTP_200_OK
        ), f"error, status: {response.status_code}"
        assert response.data == []

        # create new reviews in item1
        new_review = item1.review_set.create(
            email="test@test.test", first_name="test", last_name="test"
        )

        # test that in item1 there is one review
        response = client.get(url)
        assert (
                response.status_code == status.HTTP_200_OK
        ), f"error, status: {response.status_code}"
        assert response.data != []
        assert response.data[0]["id"] == new_review.id
        assert len(response.data) == 1

    @pytest.mark.django_db
    def test_add_review_to_item(self, initialize_task_db):
        item1 = initialize_task_db["item1"]
        url = reverse("reviews-by-item", kwargs={"item_id": item1.id})
        client = APIClient()
        response = client.post(url, data={
            "email": "email@email.email",
            "first_name": "first_name",
            "last_name": "last_name",
            "text": "text",
            "state": "pending",
            "rate_by_stars": 2
        })
        assert (
                response.status_code == status.HTTP_201_CREATED
        ), f"error, status: {response.status_code}"

        assert item1.review_set.count() == 1
