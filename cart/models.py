from django.db      import models
from product.models import Product
from user.models    import User

class Cart(models.Model):
    user       = models.ForeignKey('user.User', on_delete=models.CASCADE)
    product    = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    count      = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.name

    class Meta:
        db_table = 'carts'