import os

from PIL import Image
from io import BytesIO
from django.core.files import File
from django.db import models
from django.dispatch import receiver


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
    category = models.ForeignKey(CategoryModel, related_name='item_set', null=True, blank=True, on_delete=models.SET_NULL)
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


class ItemImageModel(models.Model):
    image = models.ImageField(upload_to='images', null=True)
    product_model = models.ForeignKey(ItemModel, related_name='images', on_delete=models.CASCADE,
                                      null=True, blank=True, default=None)


@receiver(models.signals.post_delete, sender=ItemModel)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
