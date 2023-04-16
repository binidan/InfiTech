from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.core.validators import MinValueValidator
import uuid
from django_countries.fields import CountryField

# Create your models here.
class Customer(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birth_date = models.DateField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        if self.first_name==None:
            return "ERROR-CUSTOMER NAME IS NULL"
        return self.first_name


class Address(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    country = CountryField()
    state = models.CharField(max_length=30)
    address = models.CharField(max_length=150)
    address2 = models.CharField(max_length=150, null=True)
    pincode = models.CharField(
        max_length=6,
        validators=[
            RegexValidator(
                r'^[0-9]{6}$',
                'Enter a valid pincode. It must be 6 digits.'
            ),
        ]
    )


class Category(models.Model):
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, blank =True, null=True)
    title = models.CharField(max_length=100) 
    slug = models.SlugField(null=True)

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ('slug', 'parent',)    
        verbose_name_plural = "categories"     

    def __str__(self):                           
        full_path = [self.title]                  
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' -> '.join(full_path[::-1])  


class Product(models.Model):
    def get_default_id():
        return "prd-"+str(uuid.uuid4())
    
    category = models.ManyToManyField(Category)
    id = models.CharField(max_length=45, primary_key=True, default=get_default_id, editable=False)
    name = models.CharField(max_length=100)
    price = models.DecimalField(validators=[MinValueValidator(0)], max_digits=9, decimal_places=2)
    discount = models.DecimalField(validators=[MinValueValidator(0)], max_digits=5, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    in_stock = models.BooleanField(default=True)
    image = models.ImageField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    @property
    def total_cost(self):
        cost = self.price + self.discount
        return cost

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
    @property
    def shortDesc(self):
        desc = self.description[:35]
        return desc  


class Order(models.Model):
    def get_default_id():
        return "ord-"+str(uuid.uuid4())

    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    id = models.CharField(max_length=45, primary_key=True, default=get_default_id, editable=False)
    date = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)

    def __str__(self):
        if self.id==None:
            return "ERROR-CUSTOMER NAME IS NULL"
        return self.id
    
    @property
    def order_discount(self):
        orderitems = self.item_set.all()
        total = sum((item.product.discount)*(item.quantity) for item in orderitems)
        return total
    
    @property
    def order_price(self):
        orderitems = self.item_set.all()
        total = sum(item.item_price for item in orderitems)
        return total
    
    @property
    def total_price(self):
        total = self.order_price + 4
        return total

    @property
    def order_total_items(self):
        orderitems = self.item_set.all()
        total = sum(item.quantity for item in orderitems)
        return total


class Item(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    @property
    def item_price(self):
        total = self.product.price * self.quantity
        return total   