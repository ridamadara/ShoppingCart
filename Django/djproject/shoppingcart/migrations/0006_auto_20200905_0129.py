# Generated by Django 3.1 on 2020-09-04 20:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shoppingcart', '0005_auto_20200905_0122'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='password',
        ),
        migrations.RemoveField(
            model_name='user',
            name='user_name',
        ),
    ]
