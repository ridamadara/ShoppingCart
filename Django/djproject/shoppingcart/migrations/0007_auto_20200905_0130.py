# Generated by Django 3.1 on 2020-09-04 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shoppingcart', '0006_auto_20200905_0129'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='password',
            field=models.CharField(default=0, max_length=50),
        ),
        migrations.AddField(
            model_name='user',
            name='user_name',
            field=models.CharField(default=0, max_length=50),
        ),
    ]