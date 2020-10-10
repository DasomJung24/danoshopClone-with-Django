from django.db import models

class Product(models.Model):
    name          = models.CharField(max_length=50)
    price         =  models.DecimalField(max_digits=50, decimal_places=3)
    discount_rate = models.DecimalField(max_digits=50, decimal_places=3, null=True)
    product_type  = models.ForeignKey('ProductType', on_delete=models.CASCADE, null=True)
    detail        = models.TextField()
    sub_detail    = models.TextField()
    sub_name      = models.CharField(max_length=100)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)
    category      = models.ManyToManyField('Category', through='ProductCategory')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'products'

class ProductType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'product_types'

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'categories'

class ProductCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_categories'

class Image(models.Model):
    image   = models.CharField(max_length=1000)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.image

    class Meta:
        db_table = 'images'