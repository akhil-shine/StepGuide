# Generated by Django 4.2.5 on 2023-11-22 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StepGuideApp', '0017_alter_bookcart_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookcart',
            name='size',
            field=models.PositiveIntegerField(default=1, null=True),
        ),
    ]