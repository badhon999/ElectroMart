# Generated by Django 5.1.7 on 2025-03-24 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='ar_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='products',
            name='color',
            field=models.CharField(choices=[('Black', 'Black'), ('White', 'White'), ('Red', 'Red'), ('Blue', 'Blue'), ('Green', 'Green')], default='Black', max_length=20),
        ),
        migrations.AddField(
            model_name='products',
            name='has_ar',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='products',
            name='has_vr',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='products',
            name='size',
            field=models.CharField(choices=[('XS', 'XS'), ('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL')], default='M', max_length=20),
        ),
        migrations.AddField(
            model_name='products',
            name='vr_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='order',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='products',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
