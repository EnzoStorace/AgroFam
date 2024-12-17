from django.db import models
from django.db.models.signals import post_save

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='menu_images/')
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.ManyToManyField('Category', related_name='item')
    seller = models.ManyToManyField('Seller', related_name='item')
    
    def __str__(self):
        return self.name
    
class Seller(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class OrderModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Order: {self.created_on.strftime("%b %d %I:%M %p")}'
    
    @property
    def total_price(self):
        return sum(item.subtotal for item in self.order_items.all())
    
class OrderItem(models.Model):
    order = models.ForeignKey('OrderModel', related_name='order_items', on_delete=models.CASCADE)
    item = models.ForeignKey('MenuItem', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    @property
    def subtotal(self):
        return self.item.price * self.quantity

    def __str__(self):
        return f'{self.item.name} x {self.quantity}'
    
