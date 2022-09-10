from curses import tigetflag
from datetime import datetime
from queue import Empty
from secrets import choice
from django.db import models
from django.contrib.auth.models import AbstractUser
from location_field.models.plain import PlainLocationField
from phonenumber_field.modelfields import PhoneNumberField
from geopy.geocoders import Nominatim

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
    def NumberOfOrders(self):
        orders = Orders.objects.filter(user__Email = self.Email).count()
        return orders
    def NumberOfReservations(self):
        reservations = Reservation.objects.filter(user__Email = self.Email).count()
        return reservations
    def FavoriteFood(self):
        FoodList = []
        orders = Orders.objects.filter(user__id=self.id)
        if len(orders) != 0:
            for order in orders:
                FoodList.append(order.items.name)
            return max(((item, FoodList.count(item)) for item in set(FoodList)), key=lambda a: a[1])[0]
        else:
            return "Didn't Order yet."
    def UserTotalOrdersPrice(self):
        TotalPrice = 0
        userorders = Orders.objects.filter(user=self)  
        for price in userorders:
            TotalPrice = TotalPrice + price.total_price()
        return TotalPrice
    def UserCounty(self):
        geolocator = Nominatim(user_agent="geoapiExercises")
        try:
            location = geolocator.reverse(self.location)
            print(location)
            if location != None:
                address = location.raw['address']
                country = address.get('country', '')
                return country
        except:
            return None

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
    def UserTotalOrdersPrice(self):
        TotalPrice = 0
        userorders = Orders.objects.filter(user=self.user)  
        for price in userorders:
            TotalPrice = TotalPrice + price.total_price()
        return TotalPrice



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
    def AllMessages(self):
        msgs = Messages.objects.filter(post__id = self.id )
        return msgs

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