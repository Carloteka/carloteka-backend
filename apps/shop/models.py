import os
from io import BytesIO

from django.contrib.auth import get_user_model
from django.core.files import File
from django.db import models
from django.dispatch import receiver
from PIL import Image
from rest_framework.exceptions import NotFound


class CategoryModel(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(max_length=5000)

    def __str__(self):
        return self.name


class CategoryImageModel(models.Model):
    image = models.ImageField(upload_to='images', null=True)
    product_model = models.ForeignKey(CategoryModel, related_name='image_set', on_delete=models.CASCADE,
                                      null=True, blank=True, default=None)


@receiver(models.signals.post_delete, sender=CategoryImageModel)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


class ItemModel(models.Model):
    STOCK_STATUS_CHOiCES = [
        ('IN_STOCK', 'В наявносі'),
        ('OUT_OF_STOCK', 'Немає в наявності'),
        ('BACKORDER', 'Очікується'),
        ('SPECIFIC_ORDER', 'Під замовлення'),
    ]
    name = models.CharField(max_length=128)
    price = models.FloatField()
    discounted_price = models.FloatField(default=None, null=True, blank=True)
    length = models.FloatField(default=None, null=True, blank=True)
    height = models.FloatField(default=None, null=True, blank=True)
    width = models.FloatField(default=None, null=True, blank=True)
    stock = models.CharField(
        max_length=40,
        choices=STOCK_STATUS_CHOiCES,
        default='IN_STOCK'
    )
    mini_description = models.TextField(max_length=2500)
    description = models.TextField(max_length=5000)
    category = models.ForeignKey(CategoryModel, related_name='item_set', null=True, blank=True,
                                 on_delete=models.SET_NULL)
    mini_image = models.ImageField(upload_to='images/', null=True, blank=True)
    slug = models.SlugField(max_length=100, db_index=True, unique=True)
    starts = models.FloatField(default=0)
    review_count = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        img = Image.open(self.mini_image)
        max_size = (512, 512)
        img.thumbnail(max_size, Image.LANCZOS)
        temp_thumb = BytesIO()
        img.save(temp_thumb, format='PNG')
        temp_thumb.seek(0)
        self.mini_image = File(temp_thumb, name=self.mini_image.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ItemStatsModel(models.Model):
    visits = models.BigIntegerField(default=0)
    added_to_cart = models.BigIntegerField(default=0)
    added_to_favorites = models.BigIntegerField(default=0)
    item = models.OneToOneField(
        ItemModel,
        on_delete=models.CASCADE,
        related_name='stats'
    )


class ItemImageModel(models.Model):
    image = models.ImageField(upload_to='images', null=True)
    product_model = models.ForeignKey(ItemModel, related_name='image_set', on_delete=models.CASCADE,
                                      null=True, blank=True, default=None)


@receiver(models.signals.post_delete, sender=ItemImageModel)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


@receiver(models.signals.post_delete, sender=ItemModel)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.mini_image:
        if os.path.isfile(instance.mini_image.path):
            os.remove(instance.mini_image.path)


class ShopContactsModel(models.Model):
    work_time_mo_fr = models.CharField(max_length=100)
    work_time_sa = models.CharField(max_length=100)
    work_time_su = models.CharField(max_length=100)
    admin_phone = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    viber_link = models.CharField(max_length=100)
    telegram_link = models.CharField(max_length=100)


User = get_user_model()


class OrderModel(models.Model):
    STATUS_CHOICES = [
        ('new', 'Нове замовлення'),
        ('confirmed', 'Підтверджено'),
        ('shipped', 'Відправлено'),
        ('delivered', 'Доставлено'),
        ('complete', 'Виконано'),
        ('canceled', 'Скасовано'),
    ]
    PAYMENT_CHOICES = [
        ('online', 'Оплата онлайн'),
        ('cod', 'Накладений платіж'),
        ('postpay', ' После оплата')
    ]
    DELIVERY_CHOCES = [
        ('nova_post', 'Нова пошта'),
        ('ukr_post', 'Укрпошта')
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    country = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    delivery_service = models.CharField(max_length=100, choices=DELIVERY_CHOCES)
    postoffice = models.CharField(max_length=50, null=True, blank=True)
    postbox = models.CharField(max_length=50, null=True, blank=True)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_CHOICES)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    item_set = models.ManyToManyField('ItemModel', related_name='order_set')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    no_call_back = models.BooleanField(default=False, verbose_name="Не передзвонювати")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # TODO add clear_all (look in styleguide)

    def __str__(self):
        return f'OrderModel {self.id} by {self.first_name} {self.last_name}'


class ReviewModel(models.Model):
    STATE_CHOCES = [
        ("pending", "в очікуванні"),
        ("visible", "видимий"),
        ("invisible", "невидимий")
    ]
    item = models.ForeignKey(ItemModel, related_name='review_set', on_delete=models.CASCADE)
    email = models.EmailField(max_length=255)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    state = models.CharField(choices=STATE_CHOCES, default="pending", max_length=10)
    text = models.TextField(blank=True, null=True)
    date = models.DateTimeField("create", auto_now_add=True)
    updated_at = models.DateTimeField("update", auto_now=True)
    stars = models.IntegerField(
        "stars", choices=[(i, i) for i in range(1, 6)], blank=True, null=True
    )

    def __str__(self):
        return f"Review ID: {self.id} by {self.first_name} {self.last_name}"
