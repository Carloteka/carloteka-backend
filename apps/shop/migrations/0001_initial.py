# Generated by Django 4.2.7 on 2024-03-05 03:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField(max_length=5000)),
            ],
        ),
        migrations.CreateModel(
            name='ItemModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('price', models.FloatField()),
                ('discounted_price', models.FloatField(blank=True, default=None, null=True)),
                ('length', models.FloatField(blank=True, default=None, null=True)),
                ('height', models.FloatField(blank=True, default=None, null=True)),
                ('width', models.FloatField(blank=True, default=None, null=True)),
                ('stock', models.CharField(choices=[('IN_STOCK', 'В наявносі'), ('OUT_OF_STOCK', 'Немає в наявності'), ('BACKORDER', 'Очікується'), ('SPECIFIC_ORDER', 'Під замовлення')], default='IN_STOCK', max_length=40)),
                ('mini_description', models.TextField(max_length=2500)),
                ('description', models.TextField(max_length=5000)),
                ('mini_image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('stars', models.FloatField(default=0)),
                ('review_count', models.IntegerField(default=0)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='item_set', to='shop.categorymodel')),
            ],
        ),
        migrations.CreateModel(
            name='NovaPost',
            fields=[
                ('ref', models.UUIDField(editable=False, primary_key=True, serialize=False, unique=True)),
                ('int_doc_number', models.CharField(max_length=20)),
                ('cost_on_site', models.DecimalField(decimal_places=2, max_digits=10)),
                ('estimated_delivery_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='OrderItemModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=0, verbose_name='quantity product')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.itemmodel')),
            ],
        ),
        migrations.CreateModel(
            name='ShopContactsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('work_time_mo_fr', models.CharField(max_length=100)),
                ('work_time_sa', models.CharField(max_length=100)),
                ('work_time_su', models.CharField(max_length=100)),
                ('admin_phone', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('viber_link', models.CharField(max_length=100)),
                ('telegram_link', models.CharField(max_length=100)),
                ('sender_address', models.UUIDField(blank=True, null=True)),
                ('sender_warehouse_index', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ReviewModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=255)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('state', models.CharField(choices=[('pending', 'в очікуванні'), ('visible', 'видимий'), ('invisible', 'невидимий')], default='pending', max_length=10)),
                ('text', models.TextField(blank=True, null=True)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='create')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='update')),
                ('stars', models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], null=True, verbose_name='stars')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review_set', to='shop.itemmodel')),
            ],
        ),
        migrations.CreateModel(
            name='OrderModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=20)),
                ('total_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('country', models.CharField(max_length=100)),
                ('region', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=50)),
                ('delivery_service', models.CharField(choices=[('nova_post', 'Нова пошта'), ('ukr_post', 'Укрпошта')], max_length=100)),
                ('postoffice', models.CharField(blank=True, max_length=50, null=True)),
                ('postbox', models.CharField(blank=True, max_length=50, null=True)),
                ('status', models.CharField(choices=[('new', 'Нове замовлення'), ('confirmed', 'Підтверджено'), ('shipped', 'Відправлено'), ('delivered', 'Доставлено'), ('complete', 'Виконано'), ('canceled', 'Скасовано')], default='new', max_length=20)),
                ('payment_method', models.CharField(choices=[('online', 'Оплата онлайн'), ('cod', 'Накладений платіж'), ('postpay', ' После оплата')], max_length=50)),
                ('payment_status', models.CharField(choices=[('None', 'Не оплачено'), ('error', 'error'), ('liqpay', 'Liqpay')], default='None', max_length=50)),
                ('acq_id', models.IntegerField(blank=True, null=True, verbose_name='ID еквайера')),
                ('no_call_back', models.BooleanField(default=False, verbose_name='Не передзвонювати')),
                ('comment', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('item_set', models.ManyToManyField(through='shop.OrderItemModel', to='shop.itemmodel')),
                ('nova_post', models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='nova_post', to='shop.novapost')),
            ],
        ),
        migrations.AddField(
            model_name='orderitemmodel',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.ordermodel'),
        ),
        migrations.CreateModel(
            name='ItemStatsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visits', models.BigIntegerField(default=0)),
                ('added_to_cart', models.BigIntegerField(default=0)),
                ('added_to_favorites', models.BigIntegerField(default=0)),
                ('item', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='stats', to='shop.itemmodel')),
            ],
        ),
        migrations.CreateModel(
            name='ItemImageModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to='images')),
                ('product_model', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='image_set', to='shop.itemmodel')),
            ],
        ),
        migrations.CreateModel(
            name='CategoryImageModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to='images')),
                ('product_model', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='image_set', to='shop.categorymodel')),
            ],
        ),
    ]
