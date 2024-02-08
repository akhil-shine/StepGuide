# Generated by Django 4.2.5 on 2023-11-20 15:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('StepGuideApp', '0013_rename_price_product_price_1_3_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SizeStock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=50)),
                ('stock_quantity', models.IntegerField(default=0)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='StepGuideApp.product')),
            ],
        ),
    ]