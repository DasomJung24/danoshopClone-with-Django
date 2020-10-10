from django.db      import models
from product.models import Product
from user.models    import User

class Review(models.Model):
    user       = models.ForeignKey('user.User', on_delete=models.CASCADE)
    title      = models.CharField(max_length=50)
    content    = models.CharField(max_length=1000)
    score      = models.IntegerField()
    product    = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.name

    class Meta:
        db_table = 'reviews'

class ReviewImage(models.Model):
    image = models.URLField(null=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)

    def __str__(self):
        return self.review.title

    class Meta:
        db_table = 'review_images'