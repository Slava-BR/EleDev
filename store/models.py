from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here.


class Products(models.Model):
    title = models.CharField(max_length=100)
    brand = models.ForeignKey('Brands', on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    count = models.PositiveIntegerField()
    feedback = models.PositiveIntegerField()
    product_code = models.IntegerField(primary_key=True)
    category_product = models.ManyToManyField('Categories')
    discount = models.PositiveIntegerField(null=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.title


class Categories(models.Model):
    title = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    default_characteristic = models.JSONField(null=True, blank=True)
    image = models.ImageField(upload_to="categories_image/", null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    last = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("category_view", kwargs={'category': self.slug})


class Descriptions(models.Model):
    description = models.TextField(null=False)
    product = models.OneToOneField('Products', on_delete=models.CASCADE)
    characteristic = models.JSONField()

    def __str__(self):
        return self.product


class Images(models.Model):
    product = models.ForeignKey('Products', on_delete=models.CASCADE)
    image = models.ImageField(upload_to="product_image/", null=True)

    def __str__(self):
        return self.product.title


class Brands(models.Model):
    logo = models.ImageField(upload_to="brand_image/", blank=True)
    title = models.CharField(max_length=20)
    description = models.TextField(null=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.title


class FavoritesProducts(models.Model):
    products = models.ManyToManyField("Products")
    user = models.OneToOneField(User, on_delete=models.CASCADE)


