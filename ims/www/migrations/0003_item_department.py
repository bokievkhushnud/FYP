# Generated by Django 4.1.3 on 2023-02-03 15:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("www", "0002_alter_item_category_alter_item_quantity"),
    ]

    operations = [
        migrations.AddField(
            model_name="item",
            name="department",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="www.department",
            ),
            preserve_default=False,
        ),
    ]
