# Generated by Django 3.1 on 2020-08-26 15:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shoppingcart', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('code', models.CharField(max_length=50)),
                ('salary', models.IntegerField(default=0)),
                ('contact_no', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('purchase_price', models.IntegerField(default=0)),
                ('sale_price', models.IntegerField(default=0)),
                ('stock_available', models.IntegerField(default=0)),
                ('sku', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('employee_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shoppingcart.employee')),
            ],
        ),
        migrations.CreateModel(
            name='SalesOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('employee_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shoppingcart.employee')),
            ],
        ),
        migrations.CreateModel(
            name='SaleOrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('price', models.IntegerField(default=0)),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shoppingcart.salesorder')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shoppingcart.product')),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseOrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('price', models.IntegerField(default=0)),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shoppingcart.purchaseorder')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shoppingcart.product')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('price', models.IntegerField(default=0)),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shoppingcart.product')),
            ],
        ),
    ]