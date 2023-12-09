# Generated by Django 4.2.7 on 2023-12-09 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_rename_delivery_warehouse_order_postbox_order_items_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=100)),
                ('region', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=50)),
                ('delivery_service', models.CharField(choices=[('nova_post', 'Нова пошта'), ('ukr_post', 'Укрпошта')], max_length=100)),
                ('postoffice', models.CharField(blank=True, max_length=50, null=True)),
                ('postbox', models.CharField(blank=True, max_length=50, null=True)),
                ('payment_method', models.CharField(choices=[('online', 'Оплата онлайн'), ('cod', 'Накладений платіж'), ('postpay', ' После оплата')], max_length=50)),
                ('phone_number', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('comment', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('new', 'Нове замовлення'), ('confirmed', 'Підтверджено'), ('shipped', 'Відправлено'), ('delivered', 'Доставлено'), ('complete', 'Виконано'), ('canceled', 'Скасовано')], default='new', max_length=20)),
                ('no_call_back', models.BooleanField(default=False, verbose_name='Не передзвонювати')),
                ('items', models.ManyToManyField(related_name='order_set', to='shop.itemmodel')),
            ],
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='order',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='product',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='OrderItem',
        ),
    ]
