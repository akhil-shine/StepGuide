# Generated by Django 4.2.5 on 2023-11-22 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StepGuideApp', '0015_rename_price_1_3_product_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookcart',
            name='size',
            field=models.PositiveIntegerField(default=1, null=True),
        ),
    ]