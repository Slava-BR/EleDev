# Generated by Django 4.2.2 on 2023-07-31 14:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brands',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo', models.ImageField(blank=True, upload_to='brand_image/')),
                ('title', models.CharField(max_length=20)),
                ('description', models.TextField(null=True)),
                ('slug', models.SlugField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('default_characteristic', models.JSONField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='categories_image/')),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.categories')),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('title', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('count', models.PositiveIntegerField()),
                ('feedback', models.PositiveIntegerField()),
                ('product_code', models.IntegerField(primary_key=True, serialize=False)),
                ('discount', models.PositiveIntegerField(null=True)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.brands')),
                ('category_product', models.ManyToManyField(to='store.categories')),
            ],
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to='product_image/')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.products')),
            ],
        ),
        migrations.CreateModel(
            name='Descriptions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('characteristic', models.JSONField()),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='store.products')),
            ],
        ),
    ]
