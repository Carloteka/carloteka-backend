import os

from django.db import models
from django.dispatch import receiver


class CategoryModel(models.Model):
    id_name = models.CharField(max_length=50)
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
