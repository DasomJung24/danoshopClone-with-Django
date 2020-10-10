from django.db import models

class User(models.Model):
    name       = models.CharField(max_length=50)
    email      = models.CharField(max_length=100)
    password   = models.CharField(max_length=100)
    birth      = models.IntegerField(null=True, blank=True)
    job        = models.CharField(max_length=50, null=True, blank=True)
    gender     = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'users'