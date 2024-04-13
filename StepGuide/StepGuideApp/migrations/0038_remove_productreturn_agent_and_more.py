# Generated by Django 4.2.6 on 2024-03-04 09:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('StepGuideApp', '0037_productreturn'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productreturn',
            name='agent',
        ),
        migrations.RemoveField(
            model_name='productreturn',
            name='merchant',
        ),
        migrations.AddField(
            model_name='productreturn',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]