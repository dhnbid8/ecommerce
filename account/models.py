from django.db import models
from django.contrib.auth.models import User
from product.models import Product

class Profile(models.Model):

    user = models.OneToOneField(User, related_name="Profile", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phonenumber = models.CharField(max_length=12)
    address = models.CharField(max_length=500)
    zipcode = models.CharField(max_length=11)
    created_at = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to='profile/', blank=True, null=True, default="profile/Business-User-Account-PNG-Image.png")

    likes_products = models.ManyToManyField(Product)
    
    def __str__(self):
        return self.user.username
    
    def get_profile(self):
        if self.photo:
            return 'http://127.0.0.1:8000'+self.photo.url
        return ''