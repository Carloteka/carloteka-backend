import os
from io import BytesIO

from django.contrib.auth import get_user_model
from django.core.files import File
from django.db import models
from django.dispatch import receiver
from PIL import Image
from rest_framework.exceptions import NotFound


class CategoryModel(models.Model):
    id_name = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=128)
    description = models.TextField(max_length=5000)

    def __str__(self):
        return self.id_name


class CategoryImageModel(models.Model):
    image = models.ImageField(upload_to='images', null=True)
    product_model = models.ForeignKey(CategoryModel, related_name='images', on_delete=models.CASCADE,
                                      null=True, blank=True, default=None)


@receiver(models.signals.post_delete, sender=CategoryImageModel)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


class ItemModel(models.Model):
    id_name = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=128)
    price = models.FloatField()
    discounted_price = models.FloatField(default=None, null=True, blank=True)
    length = models.FloatField(default=None, null=True, blank=True)
    height = models.FloatField(default=None, null=True, blank=True)
    width = models.FloatField(default=None, null=True, blank=True)
    in_stock = models.IntegerField(default=1)
    mini_description = models.TextField(max_length=2500)
    description = models.TextField(max_length=5000)
    visits = models.IntegerField(default=0)
    category = models.ForeignKey(CategoryModel, related_name='item_set', null=True, blank=True,
                                 on_delete=models.SET_NULL)
    mini_image = models.ImageField(upload_to='images/', null=True, blank=True)

    def save(self, *args, **kwargs):
        # Open the uploaded image
        img = Image.open(self.mini_image)

        # If the image has an alpha channel, convert it to RGB
        if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
            rgb_img = img.convert('RGB')
        else:
            rgb_img = img

        # Resize it to 512x512 or smaller, keeping aspect ratio
        max_size = (512, 512)
        rgb_img.thumbnail(max_size, Image.LANCZOS)

        # Save the image back to memory
        temp_thumb = BytesIO()
        rgb_img.save(temp_thumb, format='JPEG')
        temp_thumb.seek(0)

        # Save image field
        self.mini_image = File(temp_thumb, name=self.mini_image.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.id_name


    def get_reviews(self):
        """Return all comments belonging to this item."""
        reviews = self.review_set.all()
        return reviews


class ItemImageModel(models.Model):
    image = models.ImageField(upload_to='images', null=True)
    product_model = models.ForeignKey(ItemModel, related_name='images', on_delete=models.CASCADE,
                                      null=True, blank=True, default=None)


@receiver(models.signals.post_delete, sender=ItemModel)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


class ShopContactsModel(models.Model):
    address_text = models.CharField(max_length=100)
    address_googlemaps_link = models.CharField(max_length=100)
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

    def __str__(self):
        return f'OrderModel {self.id} by {self.first_name} {self.last_name}'


class Review(models.Model):
    STATE_CHOCES = [
        ("pending", "в очікуванні"),
        ("visible", "видимий"),
        ("invisible", "невидимий")
    ]
    item_set = models.ForeignKey(ItemModel, related_name='review_set', on_delete=models.CASCADE)
    email = models.EmailField(max_length=255)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    state = models.CharField(choices=STATE_CHOCES, default="pending", max_length=10)
    text = models.TextField(blank=True, null=True)
    date = models.DateTimeField("create", auto_now_add=True)
    updated_at = models.DateTimeField("update", auto_now=True)
    rate_by_stars = models.IntegerField(
        "rate by stars", choices=[(i, i) for i in range(1, 6)], blank=True, null=True
    )

    def __str__(self):
        return f"Review ID: {self.id} by {self.first_name} {self.last_name}"
