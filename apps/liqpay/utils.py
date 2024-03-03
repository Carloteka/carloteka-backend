from apps.shop.models import OrderModel
from apps.shop.servises import get_order_by_id


def change_order_payment_status(order_id, status, acq_id):
    order = get_order_by_id(order_id)
    if status in [i[0] for i in order.PAYMENT_STATUS]:
        order.payment_status = status
        order.acq_id = acq_id
        order.save()
