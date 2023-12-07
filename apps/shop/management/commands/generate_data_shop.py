import os
import datetime
from django.core.management.base import BaseCommand
from django.core.files import File
from apps.shop.models import CategoryModel, CategoryImageModel, ItemModel, ShopContactsModel
from django.conf import settings

class Command(BaseCommand):
    help = 'Generate entries for ShopContactsModel, CategoryModel, CategoryImageModel, and ItemModel.'

    def handle(self, *args, **options):
        # Adding data for ShopContactsModel
        contact_data = {
            'address_text': 'Вулиця приклад, 111',
            'address_googlemaps_link': 'https://maps.example.com',
            'work_time_mo_fr': '9:00 - 18:00',
            'work_time_sa': '10:00 - 16:00',
            'work_time_su': 'вихідний',
            'admin_phone': '+380730999999',
            'email': 'info@example.com',
            'viber_link': 'https://viber.example.com',
            'telegram_link': 'https://telegram.example.com'
        }

        ShopContactsModel.objects.update_or_create(defaults=contact_data)
        self.stdout.write(self.style.SUCCESS('Successfully generated data for ShopContactsModel'))

        # Parameters for CategoryModel, CategoryImageModel
        num_category_entries = 4
        category_image_filename = 'apps/shop/management/images/img_data.png'
        category_image_path = os.path.join(settings.BASE_DIR, category_image_filename)

        # Generating records for CategoryModel, CategoryImageModel
        for i in range(num_category_entries):
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
            unique_id_name = f"ID_{timestamp}_{i}"

            category = CategoryModel.objects.create(id_name=unique_id_name, name="Ім'я категорії", description="Опис категорії")
            with open(category_image_path, 'rb') as image_file:
                django_file = File(image_file)
                image_instance = CategoryImageModel(product_model=category)
                image_instance.image.save(f'image_{i}.png', django_file, save=True)

            self.stdout.write(self.style.SUCCESS(f'Image for category {category.id_name} created successfully'))

        # Parameters for ItemModel
        num_item_entries = 100
        item_image_filename = 'apps/shop/management/images/img_data.png'
        item_image_path = os.path.join(settings.BASE_DIR, item_image_filename)

        categories = CategoryModel.objects.all()
        if not categories:
            self.stdout.write(self.style.ERROR('No categories available. Please create some CategoryModel entries first.'))
            return

        # Generating records for ItemModel
        for i in range(num_item_entries):
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
            id_name = f"Ваза декоративна_{timestamp}_{i}"
            name = "Ваза"
            price = 50.0
            discounted_price = 45.0
            length = 1.5
            height = 2.0
            width = 0.5
            in_stock = 10
            mini_description = "Ваза"
            description = "Ваза"
            visits = 0
            category = categories.first() if categories else None

            item = ItemModel(
                id_name=id_name,
                name=name,
                price=price,
                discounted_price=discounted_price,
                length=length,
                height=height,
                width=width,
                in_stock=in_stock,
                mini_description=mini_description,
                description=description,
                visits=visits,
                category=category
            )

            if os.path.exists(item_image_path):
                with open(item_image_path, 'rb') as image_file:
                    django_file = File(image_file)
                    item.mini_image.save(f'mini_image_{i}.png', django_file, save=False)

            item.save()
            self.stdout.write(self.style.SUCCESS(f'Item {name} created successfully with id {id_name}'))

        self.stdout.write(self.style.SUCCESS(f'Successfully generated entries for CategoryModel, CategoryImageModel, and ItemModel'))
