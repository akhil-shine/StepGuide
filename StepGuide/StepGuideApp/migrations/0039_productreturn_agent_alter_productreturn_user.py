# Generated by Django 4.2.6 on 2024-03-04 09:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('StepGuideApp', '0038_remove_productreturn_agent_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productreturn',
            name='agent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='returned_products_received', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='productreturn',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='returned_products', to=settings.AUTH_USER_MODEL),
        ),
    ]