# Generated by Django 4.2.7 on 2024-03-02 09:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0007_rename_items_ordermodel_item_set"),
    ]

    operations = [
        migrations.AddField(
            model_name="ordermodel",
            name="payment_status",
            field=models.CharField(
                choices=[("None", "Не оплачено"), ("liqpay", "Liqpay")],
                default="None",
                max_length=50,
            ),
        ),
    ]