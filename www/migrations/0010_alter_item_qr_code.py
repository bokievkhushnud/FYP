# Generated by Django 4.1.3 on 2023-05-04 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("www", "0009_alter_category_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="qr_code",
            field=models.ImageField(blank=True, null=True, upload_to="items"),
        ),
    ]
