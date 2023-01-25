# Generated by Django 4.1.3 on 2023-01-17 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("www", "0002_item_image_alter_consumable_holder"),
    ]

    operations = [
        migrations.AddField(
            model_name="bulkitem",
            name="image",
            field=models.ImageField(default="default.png", upload_to="items"),
        ),
        migrations.AddField(
            model_name="consumable",
            name="image",
            field=models.ImageField(default="default.png", upload_to="items"),
        ),
        migrations.AlterField(
            model_name="item",
            name="image",
            field=models.ImageField(default="default.png", upload_to="items"),
        ),
    ]
