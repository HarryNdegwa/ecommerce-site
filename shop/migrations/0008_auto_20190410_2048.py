# Generated by Django 2.0.7 on 2019-04-10 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_auto_20190409_1927'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='item',
        ),
        migrations.AlterField(
            model_name='order',
            name='client_id',
            field=models.IntegerField(unique=True),
        ),
    ]
