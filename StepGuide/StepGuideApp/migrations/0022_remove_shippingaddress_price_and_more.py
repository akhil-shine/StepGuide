# Generated by Django 4.2.5 on 2023-11-30 06:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('StepGuideApp', '0021_shippingaddress'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shippingaddress',
            name='price',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='size',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='total_price',
        ),
    ]
