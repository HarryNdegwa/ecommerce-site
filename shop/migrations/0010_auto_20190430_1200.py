# Generated by Django 2.0.7 on 2019-04-30 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_auto_20190415_0740'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='client_id',
            field=models.CharField(max_length=8),
        ),
    ]
