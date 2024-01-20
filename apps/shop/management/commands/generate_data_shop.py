import os
from django.db import transaction
import random
from django.core.management.base import BaseCommand
from django.core.files import File
from apps.shop.models import CategoryModel, CategoryImageModel, ItemModel, ShopContactsModel, ItemImageModel
from django.conf import settings
from random import randint

num_category_entries = 2


class Command(BaseCommand):
    help = 'Generate entries for ShopContactsModel, CategoryModel, CategoryImageModel, ItemModel and ItemImageModel.'

    def handle(self, *args, **options):
        self.shop_contacts()
        self.category()
        self.item()

    def shop_contacts(self):
        contact_data = {
            'work_time_mo_fr': '9:00 - 18:00',
            'work_time_sa': '10:00 - 16:00',
            'work_time_su': 'вихідний',
            'admin_phone': '+380730999999',
            'email': 'info@example.com',
            'viber_link': 'https://viber.example.com',
            'telegram_link': 'https://telegram.example.com'
        }

        ShopContactsModel.objects.update_or_create(**contact_data)

    def category(self):
        existing_categories = CategoryModel.objects.all()
        if len(existing_categories) >= 2:
            pass

        else:
            categories_data = [
                {
                    'name': "Дерев'яні мечі, щити, катани, шаблі",
                    'description': "Тут ви знайдете різну дерев'яну зроброю, таку як: Мечі, Шити, Катани, Саблі, Шашки, "
                                   "на будь який смак та рік, від невеликих вакідзасі для дітей, до великих двохметрових "
                                   "мечів, які підніме тількі людина із стальними м'язами",
                    "image_path": "apps/shop/management/img/category/sward.png"
                },
                {
                    'name': "Шахи, шашки, нарди",
                    'description': "У цій категорії ви знайдете шахи, шкаки, та нарди. Всі вони виключно преміальної якості"
                                   "виготовленя вручну нашими майстрами",
                    "image_path": "apps/shop/management/img/category/chess.jpg"
                }
            ]

            for i in categories_data:
                category = CategoryModel.objects.create(name=i['name'], description=i['description'])
                with open(os.path.join(settings.BASE_DIR, i['image_path']), 'rb') as image_file:
                    django_file = File(image_file)
                    image_instance = CategoryImageModel(product_model=category)
                    image_instance.image.save(f'image_{i["name"]}.png', django_file, save=True)

    def item(self):

        def generate_items(n, theme, category_name, stock_distribution):
            # Отримуємо категорію з бази даних
            category = CategoryModel.objects.get(name=category_name)

            for i in range(n):
                name = f'{theme} #{i + 1}'
                price = round(random.uniform(100, 1000), 2)
                length = random.uniform(50, 200)
                stock = stock_distribution[i % len(stock_distribution)]
                mini_description = f'Це {theme.lower()} з унікальним дизайном.'
                description = (f'{name} - це високоякісний {theme.lower()} з унікальним дизайном. Він виготовлений'
                               f' з високоякісних матеріалів і має привабливий вигляд.')
                slug = f'{theme.lower()}-{i + 1}'

                # Відкриваємо файл зображення
                with open(f'apps/shop/management/img/sward.png', 'rb') as img_file:
                    # Створюємо новий екземпляр моделі ItemModel
                    item = ItemModel(
                        name=name,
                        price=price,
                        length=length,
                        stock=stock,
                        mini_description=mini_description,
                        description=description,
                        slug=slug,
                        category=category,
                        mini_image=File(img_file),
                    )

                    # Зберігаємо об'єкт в базі даних
                    item.save()

                    # Додаємо три зображення до товару
                    for _ in range(3):
                        item_image = ItemImageModel(image=File(img_file), product_model=item)
                        item_image.save()

                    # Друкуємо повідомлення в консолі
                    print(f'Товар "{name}" було успішно згенеровано та збережено в базі даних.')

        stock_distribution = ['IN_STOCK'] * 75 + ['OUT_OF_STOCK'] * 25 + ['BACKORDER'] * 25 + ['SPECIFIC_ORDER'] * 25

        with transaction.atomic():
            categories = CategoryModel.objects.all()
            for category in categories:
                generate_items(150, category.name, category.name, stock_distribution)
