from apps.shop.models import OrderModel, OrderItemModel, ItemModel
from rest_framework import exceptions


def get_item_by_id(item_id):
    try:
        item = ItemModel.objects.get(id=item_id)
    except ItemModel.DoesNotExist:
        raise exceptions.ValidationError({"detail": "Item not found"})
    return item


def get_order_by_id(item_id):
    try:
        order = OrderModel.objects.get(id=item_id)
    except ItemModel.DoesNotExist:
        raise exceptions.ValidationError({"detail": "Item not found"})
    return order


def order_create(*args, **kwargs):
    items = kwargs.pop("items")
    obj = OrderModel(**kwargs)
    obj.full_clean()
    obj.save()

    for item in items:
        item_obj = get_item_by_id(item.get("item"))
        quantity = item.get("quantity")
        OrderItemModel(order=obj, item=item_obj, quantity=quantity).save()
    return obj
