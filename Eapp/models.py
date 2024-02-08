from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField
from cart.cart import Cart


# Create your models here.
class Categories(models.Model):
    name=models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Colour(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Contact_us(models.Model):
    name=models.CharField(max_length=30)
    email=models.EmailField(max_length=100)
    subject=models.TextField()
    message=models.TextField
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

    def __str__(self):
        return self.name


class Filter_Price(models.Model):
    FILTER_PRICE = (
        ('100 TO 1000', '100 TO 1000'),
        ('1000 TO 10000', '1000 TO 10000'),
        ('10000 TO 20000', '10000 TO 20000'),
        ('20000 TO 30000', '20000 TO 30000'),
        ('30000 TO 40000', '30000 TO 40000'),
        ('50000 TO 100000', '50000 TO 100000'),
        ('100000 TO 1000000', '100000 TO 1000000')
    )

    price = models.CharField(choices=FILTER_PRICE, max_length=60)

    def __str__(self):
        return self.price


class Product(models.Model):
    CONDITION = (('New', 'New'), ('Old', 'Old'))
    STOCK = (('IN STOCK', 'IN STOCK'), ('OUT OF STOCK', 'OUT OF STOCK'))
    STATUS = (('Publish', 'Publish'), ('draft', 'draft'))
    OFFER=(('YES','YES'),('N0','NO'))

    image = models.ImageField(upload_to='Product_images/img')
    image2 = models.ImageField(upload_to='Product_images/img', null=True)
    image3 = models.ImageField(upload_to='Product_images/img', null=True)
    image4 = models.ImageField(upload_to='Product_images/img', null=True)

    name = models.CharField(max_length=200)
    price = models.IntegerField()
    discount=models.IntegerField(default=0,null=True)
    condtion = models.CharField(choices=CONDITION, max_length=100)
    information = RichTextField(null=True)
    description = RichTextField(null=True)
    quantity = models.IntegerField(default=10)
    offer=models.CharField(choices=OFFER,max_length=10,default='NO')
    stock = models.CharField(choices=STOCK, max_length=30)
    status = models.CharField(choices=STATUS, max_length=20)
    priority = models.IntegerField(default=0)
    create_at = models.DateField(default=timezone.now)
    updated_at = models.DateField(auto_now=True)

    categories = models.ForeignKey(Categories, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    colour = models.ForeignKey(Colour, on_delete=models.CASCADE)
    filter_price = models.ForeignKey(Filter_Price, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def __iter__(self):
        # You may need to customize this based on your requirements
        yield self.name
        yield self.price



class Tag(models.Model):
        name = models.CharField(max_length=200)
        product = models.ForeignKey(Product, on_delete=models.CASCADE)

        def __str__(self):
            return  self.name



class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    firstname=models.CharField(max_length=100)
    lastname=models.CharField(max_length=100)
    country=models.CharField(max_length=100)
    address=models.TextField()
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    postcode=models.IntegerField()
    phone=models.IntegerField()
    email=models.EmailField()
    amount=models.CharField(max_length=1000)
    paymentid=models.CharField(max_length=300,null=True,blank=True)
    paid=models.BooleanField(default=False,null=True)
    date=models.DateField(auto_now=True)

    def __str__(self):
        return self.user.username

class Orderitem(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    product=models.CharField(max_length=200)
    image=models.ImageField(upload_to='product_images/order_img')
    quantity=models.CharField(max_length=20)
    price=models.CharField(max_length=40)
    total=models.CharField(max_length=1000)
    date_added=models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.order.user.username

class review(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    item=models.ForeignKey(Product,on_delete=models.CASCADE)
    review_desp=models.CharField(max_length=700)
    ratings=models.IntegerField()

    def __str__(self):
        return str(self.user)

class wishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,default=True)
    products=models.ForeignKey(Product,on_delete=models.CASCADE,default=True)
