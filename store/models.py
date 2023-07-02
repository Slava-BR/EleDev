from django.db import models


# Create your models here.


def default_distinctive_features():
    return {
        "color": "",
        "diagonal": "",
        "memory": "",
        "volume": ""
    }


class Products(models.Model):
    title = models.CharField(max_length=50)
    producer = models.ForeignKey('Producer', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    count = models.PositiveIntegerField()
    feedback = models.PositiveIntegerField()
    product_code = models.SmallIntegerField(primary_key=True)
    distinctive_features = models.JSONField(default=default_distinctive_features)

    def __str__(self):
        return self.title


class Categories(models.Model):
    title = models.CharField(max_length=50)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title


class Descriptions(models.Model):
    description = models.TextField(null=False)
    product = models.OneToOneField('Products', on_delete=models.CASCADE)


class Images(models.Model):
    electronic_devices = models.ForeignKey('Products', on_delete=models.CASCADE)
    image = models.ImageField(null=True)


class GroupsCharacteristics(models.Model):
    description = models.ForeignKey('Descriptions', on_delete=models.CASCADE)
    name_group = models.CharField(max_length=20)

    def __str__(self):
        return self.name_group


class Fields(models.Model):
    name = models.CharField(max_length=20)
    value = models.CharField(max_length=20)
    gc = models.ForeignKey('GroupsCharacteristics', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Producer(models.Model):
    logo = models.ImageField()
    title = models.CharField(max_length=20)
    description = models.TextField()

    def __str__(self):
        return self.title
