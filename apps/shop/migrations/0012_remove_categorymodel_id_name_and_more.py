# Generated by Django 4.2.7 on 2024-01-19 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0011_remove_reviewmodel_rate_by_stars_reviewmodel_stars'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categorymodel',
            name='id_name',
        ),
        migrations.RemoveField(
            model_name='itemmodel',
            name='id_name',
        ),
        migrations.AddField(
            model_name='itemstatsmodel',
            name='added_to_cart',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='itemstatsmodel',
            name='added_to_favorites',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='categorymodel',
            name='id',
            field=models.CharField(max_length=50, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='itemmodel',
            name='id',
            field=models.CharField(max_length=128, primary_key=True, serialize=False, unique=True),
        ),
    ]
