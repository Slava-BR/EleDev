from django.contrib import admin
from store.models import *


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ['title']
    prepopulated_fields = {'slug': ('title',)}


class ProductsAdmin(admin.ModelAdmin):
    list_display = ['title']
    prepopulated_fields = {'slug': ('product_code',)}


class BrandsAdmin(admin.ModelAdmin):
    list_display = ['title']
    prepopulated_fields = {'slug': ('title',)}


# Register your models here.
admin.site.register(Brands, BrandsAdmin)
admin.site.register(Products, ProductsAdmin)
admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Images)
admin.site.register(Descriptions)
admin.site.register(FavoritesProducts)



