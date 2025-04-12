# Generated by Django 4.2.7 on 2025-04-12 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_stockmovement'),
    ]

    operations = [
        migrations.AddField(
            model_name='seller',
            name='role',
            field=models.CharField(choices=[('seller', 'Seller'), ('manager', 'Manager')], default='seller', max_length=20),
        ),
    ]
