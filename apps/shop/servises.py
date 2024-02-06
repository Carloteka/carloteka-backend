from apps.shop.models import OrderModel, OrderItemModel, ItemModel, ReviewModel
from rest_framework import exceptions


def get_item_by_id(item_id):
    try:
        item = ItemModel.objects.get(id=item_id)
    except ItemModel.DoesNotExist:
        raise exceptions.NotFound({"detail": "Item not found"})
    return item


def get_order_by_id(item_id):
    try:
        order = OrderModel.objects.get(id=item_id)
    except ItemModel.DoesNotExist:
        raise exceptions.NotFound({"detail": "Order not found"})
    return order


def order_create(*args, **kwargs) -> OrderModel:
    items = kwargs.pop("items")
    obj = OrderModel(**kwargs)
    obj.full_clean()
    obj.save()

    for item in items:
        item_obj = get_item_by_id(item.get("item"))
        quantity = item.get("quantity")
        OrderItemModel(order=obj, item=item_obj, quantity=quantity).save()
    return obj


def review_create(item_id: int, **kwargs) -> ReviewModel:
    item = get_item_by_id(item_id=item_id)
    review_obj = ReviewModel(item=item, **kwargs)
    review_obj.full_clean()
    review_obj.save()
    return review_obj
