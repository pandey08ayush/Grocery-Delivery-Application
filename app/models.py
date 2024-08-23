from django.db import models
from django.contrib.auth.models import User

STATES_CHOICES= (
        ('AN', 'Andaman and Nicobar Islands'),
        ('AP', 'Andhra Pradesh'),
        ('AR', 'Arunachal Pradesh'),
        ('AS', 'Assam'),
        ('BR', 'Bihar'),
        ('CH', 'Chandigarh'),
        ('CT', 'Chhattisgarh'),
        ('DN', 'Dadra and Nagar Haveli'),
        ('DD', 'Daman and Diu'),
        ('DL', 'Delhi'),
        ('GA', 'Goa'),
        ('GJ', 'Gujarat'),
        ('HR', 'Haryana'),
        ('HP', 'Himachal Pradesh'),
        ('JK', 'Jammu and Kashmir'),
        ('JH', 'Jharkhand'),
        ('KA', 'Karnataka'),
        ('KL', 'Kerala'),
        ('LD', 'Lakshadweep'),
        ('MP', 'Madhya Pradesh'),
        ('MH', 'Maharashtra'),
        ('MN', 'Manipur'),
        ('ML', 'Meghalaya'),
        ('MZ', 'Mizoram'),
        ('NL', 'Nagaland'),
        ('OR', 'Odisha'),
        ('PY', 'Puducherry'),
        ('PB', 'Punjab'),
        ('RJ', 'Rajasthan'),
        ('SK', 'Sikkim'),
        ('TN', 'Tamil Nadu'),
        ('TS', 'Telangana'),
        ('TR', 'Tripura'),
        ('UP', 'Uttar Pradesh'),
        ('UK', 'Uttarakhand'),
        ('WB', 'West Bengal'),
)

class Customer(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality=models.CharField(max_length=150)
    city=models.CharField(max_length=150)
    zipcode=models.IntegerField()
    state=models.CharField(choices=STATES_CHOICES, max_length=50)

    def __str__(self):
        return str(self.id)


CATEGORY_CHOICES= (
        ('M', 'Flour'),
        ('L', 'Oil and Ghee'),
        ('TW', 'Personal Care'),
        ('BW', 'Dairy and Breakfast'),
)

class Product(models.Model):
    title = models.CharField(max_length=200)
    selling_price=models.FloatField()
    discount_price=models.FloatField()
    decsription=models.TextField()
    brand=models.CharField(max_length=150)
    category=models.CharField(choices=CATEGORY_CHOICES, max_length=10)
    product_image=models.ImageField(upload_to='products')
    
    def __str__(self):
        return str(self.id)

class Cart(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    product=models.ForeignKey( Product, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
    
#     @property
#     def total_cost(self):
#         return self.quantity * self.product.discount_price

STATUS_CHOICES = (
        ('Accepted', 'Accepted'),
        ('Packed', 'Packed'),
        ('DELIVERED', 'Delivered'),
        ('RETURNED', 'Returned'),
)
class orderplaced(models.Model):
     user=models.ForeignKey(User, on_delete=models.CASCADE)
     customer=models.ForeignKey(Customer, on_delete=models.CASCADE)
     product=models.ForeignKey( Product, on_delete=models.CASCADE)
     quantity=models.PositiveIntegerField(default=1)
     order_dated=models.DateTimeField(auto_now_add=True)
     status=models.CharField(choices=STATUS_CHOICES,max_length=100)



        

# Create your models here.