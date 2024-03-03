import os
from django.db import transaction
import random
from django.core.management.base import BaseCommand
from django.core.files import File
from apps.shop.models import (
    CategoryModel,
    CategoryImageModel,
    ItemModel,
    ShopContactsModel,
    ItemImageModel,
    ItemStatsModel,
    ReviewModel,
    OrderModel,
    OrderItemModel,
)
from django.conf import settings
from datetime import timedelta
from django.utils import timezone
from faker import Faker

num_category_entries = 2


class Command(BaseCommand):
    help = 'Generate entries for ShopContactsModel, CategoryModel, CategoryImageModel, ItemModel and ItemImageModel.'
    count_orders = 10
    @transaction.atomic()
    def handle(self, *args, **options):
        self.shop_contacts()
        self.category()
        self.item()
        self.item_images()
        self.item_stats()
        self.review()
        self.generate_order()

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
            with open(f'apps/shop/management/img/sward_mini.webp', 'rb') as img_file:
                item_set = []
                for i in range(n):
                    name = f'{theme} #{i + 1}'
                    price = round(random.uniform(100, 1000), 2)
                    length = random.uniform(50, 200)
                    stock = stock_distribution[i % len(stock_distribution)]
                    mini_description = f'Це {theme.lower()} з унікальним дизайном.'
                    description = (f'{name} - це високоякісний {theme.lower()} з унікальним дизайном. '
                                   f'Він виготовлений з вищого сорту дерева, '
                                   f'має розмір {length} см, що робить його ідеальним для зручного використання. '
                                   f'Цей {theme.lower()} виконаний з великою увагою до деталей, '
                                   f'що підкреслює його високу якість та унікальність. '
                                   f'Він виготовлений з високоякісних матеріалів, '
                                   f'що гарантують його довговічність та надійність. '
                                   f'Цей {theme.lower()} є відмінним доповненням до будь-якої колекції '
                                   f'або може слугувати прекрасним подарунком. '
                                   f'Він виготовлений з високоякісного дерева, '
                                   f'що додає йому естетичної привабливості та вишуканості. '
                                   f'Цей {theme.lower()} є не тільки практичним предметом, '
                                   f'але й відмінним елементом декору. '
                                   f'Він виготовлений з високоякісних матеріалів і має привабливий вигляд.')

                    slug = f'{theme.lower()}-{i + 1}'

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
                        stars=random.randint(1, 6)
                    )
                    item_set.append(item)
                    print(f'Товар "{name}" було успішно згенеровано та збережено в базі даних.')
                ItemModel.objects.bulk_create(item_set)

        stock_distribution = ['IN_STOCK'] * 75 + ['OUT_OF_STOCK'] * 25 + ['BACKORDER'] * 25 + ['SPECIFIC_ORDER'] * 25

        if len(ItemModel.objects.all()) >= 299:
            pass
        else:
            categories = CategoryModel.objects.all()
            for category in categories:
                generate_items(150, category.name, category.name, stock_distribution)

    def item_images(self):
        item_set = ItemModel.objects.all()
        with open(f'apps/shop/management/img/sward.png', 'rb') as img_file:
            image_file = File(img_file)
            for item in item_set:
                item_image = ItemImageModel(image=image_file, product_model=item)
                item_image.save()

    def item_stats(self):
        def generate_item_stats():
            stats = ItemStatsModel.objects.all()
            if len(stats) > 50:
                pass

            else:
                items = ItemModel.objects.all()

                for item in items:
                    visits = random.randint(30000, 500000)
                    added_to_cart = random.randint(750, 10000)
                    added_to_favorites = random.randint(750, 10000)

                    item_stats = ItemStatsModel(
                        visits=visits,
                        added_to_cart=added_to_cart,
                        added_to_favorites=added_to_favorites,
                        item=item
                    )

                    item_stats.save()

                    print(f'Статистика для товару "{item.name}" була успішно згенерована та збережена в базі даних.')

        generate_item_stats()

    def review(self):
        def generate_review_data():
            # Predefined Ukrainian texts
            ukrainian_texts = [
                "Це чудовий продукт!",
                "Я вражений якістю цього товару.",
                "Не рекомендую цей продукт.",
                "Цей товар не вартує своєї ціни.",
                "Я обов'язково куплю це знову!"
            ]

            # Get all items
            items = ItemModel.objects.all()

            for item in items:
                # Generate a random number of reviews for each item
                for _ in range(random.randint(3, 30)):
                    # Generate data
                    email = f"{random.randint(1, 1000)}@example.com"
                    first_name = "Ім'я" + str(random.randint(1, 100))
                    last_name = "Прізвище" + str(random.randint(1, 100))
                    state = random.choice(["pending", "visible", "invisible"])
                    text = random.choice(ukrainian_texts)
                    stars = random.randint(1, 5)

                    # Generate a random date between 1 year ago and yesterday
                    one_year_ago = timezone.now() - timedelta(days=365)
                    yesterday = timezone.now() - timedelta(days=1)
                    date = one_year_ago + (yesterday - one_year_ago) * random.random()
                    updated_at = timezone.now()

                    # Create and save the review
                    review = ReviewModel(
                        item=item,
                        email=email,
                        first_name=first_name,
                        last_name=last_name,
                        state=state,
                        text=text,
                        date=date,
                        updated_at=updated_at,
                        stars=stars,
                    )
                    review.save()

        generate_review_data()

    def generate_order(self):
        fake = Faker("uk_UA")
        items = ItemModel.objects.all()

        def create_order():
            order = OrderModel.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                phone_number="068" + str(random.randint(1000000, 9999999)),
                country="UA",
                region=fake.region(),
                city=fake.city_name(),
                delivery_service=random.choice(("nova_post", "ukr_post")),
                status=random.choice(('new', 'confirmed', 'shipped', 'delivered', 'complete', 'canceled')),
                payment_method=random.choice(("online, postpay")),
                payment_status=random.choice(("None", 'error', 'liqpay')),
                no_call_back=bool(random.randint(0, 1))
            )
            return order

        if len(OrderModel.objects.all()) < self.count_orders:
            for i in range(self.count_orders):
                _order = create_order()
                item1 = random.choice(items)
                order_item1 = OrderItemModel.objects.create(
                    order=_order,
                    item=item1,
                    quantity=2,
                )
                _order.total_amount = order_item1.quantity * item1.price
                _order.save()
                print(f"Order {_order.id} generated.")
