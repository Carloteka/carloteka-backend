# Generated by Django 4.2.7 on 2024-02-21 22:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0007_rename_items_ordermodel_item_set"),
    ]

    operations = [
        migrations.CreateModel(
            name="NovaPost",
            fields=[
                (
                    "ref",
                    models.UUIDField(
                        editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("int_doc_number", models.CharField(max_length=20)),
                ("cost_on_site", models.DecimalField(decimal_places=2, max_digits=5)),
                ("estimated_delivery_date", models.DateField()),
            ],
        ),
        migrations.AddField(
            model_name="ordermodel",
            name="nova_post",
            field=models.OneToOneField(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="nova_post",
                to="shop.novapost",
            ),
        ),
    ]