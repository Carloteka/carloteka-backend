# Generated by Django 4.2.7 on 2023-11-16 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_itemmodel_mini_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShopContactsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_text', models.CharField(max_length=100)),
                ('address_googlemaps_link', models.CharField(max_length=100)),
                ('work_time_mo_fr', models.CharField(max_length=100)),
                ('work_time_sa', models.CharField(max_length=100)),
                ('work_time_su', models.CharField(max_length=100)),
                ('admin_phone', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('viber_link', models.CharField(max_length=100)),
                ('telegram_link', models.CharField(max_length=100)),
            ],
        ),
    ]