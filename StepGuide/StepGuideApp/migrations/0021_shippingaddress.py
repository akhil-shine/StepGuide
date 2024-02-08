# Generated by Django 4.2.5 on 2023-11-30 06:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('StepGuideApp', '0020_alter_bookcart_size'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShippingAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('phn1', models.CharField(max_length=15)),
                ('phn2', models.CharField(blank=True, max_length=15, null=True)),
                ('address', models.TextField()),
                ('country', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=255)),
                ('district', models.CharField(max_length=255)),
                ('pin', models.CharField(max_length=10)),
                ('land', models.CharField(blank=True, max_length=255, null=True)),
                ('city', models.CharField(blank=True, max_length=15, null=True)),
                ('quantity', models.PositiveIntegerField()),
                ('price', models.DecimalField(decimal_places=2, default=1, max_digits=10)),
                ('total_price', models.DecimalField(decimal_places=2, default=1, max_digits=10)),
                ('size', models.PositiveIntegerField(default=1, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='StepGuideApp.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]