# Generated by Django 4.2.6 on 2024-04-06 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StepGuideApp', '0039_productreturn_agent_alter_productreturn_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Shipped', 'Shipped'), ('Out_for_delivery', 'Out for Delivery'), ('Delivered', 'Delivered')], default='Pending', max_length=20),
        ),
    ]
