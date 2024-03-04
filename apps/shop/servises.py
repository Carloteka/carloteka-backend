from decimal import Decimal
from django.db import connection

from rest_framework import exceptions

from apps.shop.models import ItemModel, OrderItemModel, OrderModel, ReviewModel, NovaPost


def get_item_by_id(item_id):
    try:
        item = ItemModel.objects.get(id=item_id)
    except ItemModel.DoesNotExist:
        raise exceptions.NotFound({"detail": "Item not found"})
    return item


def get_order_by_id(item_id):
    try:
        order = OrderModel.objects.get(id=item_id)
    except OrderModel.DoesNotExist:
        raise exceptions.NotFound({"detail": "Order not found"})
    return order


def order_create(*args, **kwargs) -> OrderModel:
    items = kwargs.pop("items")

    waybill: dict | None = kwargs.pop("waybill_np", None)
    if waybill:
        waybill_np_obj = NovaPost(ref=waybill["ref"],
                                  int_doc_number=waybill["int_doc_number"],
                                  cost_on_site=waybill["cost_on_site"],
                                  estimated_delivery_date=waybill["estimated_delivery_date"])
        waybill_np_obj.save()
    else:
        waybill_np_obj = None

    # calculating the actual sum of prices of goods multiplied by quantity
    sum_amount = Decimal(
        sum(
            [
                (item.get("quantity") * get_item_by_id(item.get("item")).price)
                for item in items
            ]
        )
    ).quantize(Decimal("1.00"))
    # checking the correspondence of the received and fictitiously defended amount
    if sum_amount != kwargs.get("total_amount"):
        raise exceptions.ValidationError(
            {"total_amount": f"Total amount is not correct. Should be {sum_amount}"}
        )
    obj = OrderModel(nova_post=waybill_np_obj, **kwargs)
    obj.full_clean()
    obj.save()

    for item in items:
        item_obj = get_item_by_id(item.get("item"))
        quantity = item.get("quantity")
        OrderItemModel(order=obj, item=item_obj, quantity=quantity).save()

    return obj


def review_create(item_id: int, **kwargs) -> ReviewModel:
    item = get_item_by_id(item_id=item_id)
    user_email = kwargs.get("email")

    # Checking the ability to leave a review
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT DISTINCT item_id  "
            "FROM shop_ordermodel "
            "JOIN shop_orderitemmodel ON shop_ordermodel.id = shop_orderitemmodel.order_id "
            f"WHERE shop_ordermodel.email = '{user_email}';"
        )
        available_items = [i[0] for i in cursor.fetchall()]  # list of item_id for which the user can leave a review
    if item.id not in available_items:
        raise exceptions.PermissionDenied(
            {"detail": "The user did not buy this product"}
        )

    review_obj = ReviewModel(item=item, **kwargs)
    review_obj.full_clean()
    review_obj.save()
    return review_obj
