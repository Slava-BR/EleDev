from django.db import models


# Create your models here.


class Products(models.Model):
    title = models.CharField(max_length=50)
    producer = models.ForeignKey('Producer', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    count = models.PositiveIntegerField()
    feedback = models.PositiveIntegerField()
    product_code = models.IntegerField(primary_key=True)
    category_product = models.ForeignKey('Categories', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Categories(models.Model):
    title = models.CharField(max_length=50)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    default_characteristic = models.JSONField()

    def __str__(self):
        return self.title


class Descriptions(models.Model):
    description = models.TextField(null=False)
    product = models.OneToOneField('Products', on_delete=models.CASCADE)
    characteristic = models.JSONField()

    def __str__(self):
        return self.product


class Images(models.Model):
    product = models.ForeignKey('Products', on_delete=models.CASCADE)
    image = models.ImageField(null=True)

    def __str__(self):
        return self.product.title + self.image_id


class Producer(models.Model):
    logo = models.ImageField()
    title = models.CharField(max_length=20)
    description = models.TextField()

    def __str__(self):
        return self.title
