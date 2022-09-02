from curses import tigetflag
from datetime import datetime
from queue import Empty
from secrets import choice
from django.db import models
from django.contrib.auth.models import AbstractUser
from location_field.models.plain import PlainLocationField
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):

    pic = models.ImageField(null = True , default="profile-7.jpg")
    Email = models.EmailField(unique=True)
    name = models.CharField(max_length=200, null = True)
    location = PlainLocationField(based_fields=['Cairo'], zoom=7)
    phone_number = PhoneNumberField(null=True)
    # UserOrders = models.ForeignKey("Orders", related_name=("userorders"),null=True, on_delete= models.CASCADE)
    USERNAME_FIELD = 'Email'
    REQUIRED_FIELDS = []
    
    def role(self):
        return str(self.groups.all()[0])


class Items(models.Model):
    FOOD_CHOICES = (
    ("denner", "denner"),
    ("lunch", "lunch"),
    ("drinks", "drinks"),
 
)
    
    name = models.CharField(max_length=200)
    image = models.ImageField(default = 'post-img-03.jpg')
    quantity = models.IntegerField(default= 1)
    description = models.TextField(default='Great test food')
    price = models.FloatField(default=1.99)
    type = models.CharField(max_length=10,choices= FOOD_CHOICES, default= "lunch")
    def __str__(self):
        return self.name

class Orders(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    items = models.ForeignKey(Items, on_delete=models.CASCADE)
    user = models.ForeignKey(User ,on_delete = models.CASCADE )
    more_information = models.TextField(null=True)
    quantity = models.IntegerField(default=1)
    def __str__(self):
        return str(self.items)
    def total_price(self):
        return int(self.quantity * self.items.price)
    def prograss(self):
        return int(self.quantity * self.items.price) * 10


class Reservation(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    members = models.IntegerField()
    table_number = models.IntegerField(null=True)
    Reservation_time = models.CharField(max_length=200)
    
    def __str__(self):
        return self.Reservation_time
    def prograss(self):
        return self.members * 10

class Posts(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    tag = models.CharField(max_length=200,null = True)
    pic = models.ImageField(null = True , default="img-07.jpg")
    def __str__(self):
        return self.title

class Messages(models.Model):
    post = models.ForeignKey(Posts, on_delete= models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    body = models.TextField()
    def __str__(self):
        return self.body[0:20]

class Contact(models.Model):
    message = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.message[0:20]

class ToDoList(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=True)
    body = models.CharField(max_length=500)
    compeleted = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.body[0:20]
    # def compeletedtime(self):
    #     if self.compeleted == True:
    #         compeletedTime = datetime.now().minute
    #     return compeletedTime
    # def automaticDelete(self, *args , **kwargs):
    #     if self.compeletedtime == datetime.now().minute + 1 :
    #         self.delete()