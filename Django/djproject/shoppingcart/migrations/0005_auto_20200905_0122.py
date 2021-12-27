# Generated by Django 3.1 on 2020-09-04 20:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shoppingcart', '0004_product_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=100)),
                ('address_line1', models.CharField(max_length=100)),
                ('address_line2', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('district', models.CharField(max_length=100)),
                ('post_code', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Cateogary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.TextField(default=1, max_length=500),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='item',
            name='product_id',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='shoppingcart.product'),
        ),
        migrations.AlterField(
            model_name='product',
            name='purchase_price',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='sale_price',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='stock_available',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='employee_id',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='shoppingcart.employee'),
        ),
        migrations.AlterField(
            model_name='purchaseorderitem',
            name='order_id',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='shoppingcart.purchaseorder'),
        ),
        migrations.AlterField(
            model_name='purchaseorderitem',
            name='product_id',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='shoppingcart.product'),
        ),
        migrations.AlterField(
            model_name='saleorderitem',
            name='order_id',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='shoppingcart.salesorder'),
        ),
        migrations.AlterField(
            model_name='saleorderitem',
            name='product_id',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='shoppingcart.product'),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('billing_address', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='billing_address', to='shoppingcart.address')),
                ('shipping_address', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='shipping_address', to='shoppingcart.address')),
                ('user_id', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='shoppingcart.user')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='cateogary',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='shoppingcart.cateogary'),
        ),
    ]