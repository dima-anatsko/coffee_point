# Generated by Django 3.0.6 on 2020-05-26 11:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0006_auto_20200520_2231'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ('created_at',), 'verbose_name': 'Заказ', 'verbose_name_plural': 'заказы'},
        ),
    ]
