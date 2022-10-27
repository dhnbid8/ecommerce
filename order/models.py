from django.contrib.auth.models import User
from django.db import models
from product.models import Product

class OrderItem(models.Model):
    product = models.ForeignKey(Product, related_name="OrderItem", on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
    	return f'{self.product.name}  {self.quantity}'

class Order(models.Model):
    user = models.ForeignKey(User, related_name='order', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    created_at = models.DateField(auto_now_add=True)
    paid_amount = models.DecimalField(max_digits=8,decimal_places=2,blank=True,null=True)
    
    items = models.ManyToManyField(OrderItem)

    STATUS_CHOICES = (
        ('PP', 'در انتظار پرداخت'),
        ('PE', 'درحال بررسی'),
        ('RS', 'آماده ی ارسال'),
        ('PO', 'ارسال شده'),
    )
    status = models.CharField(max_length=300, choices=STATUS_CHOICES, default='PP')
    
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
