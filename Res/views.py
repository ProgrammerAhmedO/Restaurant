from datetime import datetime
from multiprocessing import context
from urllib import request
from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

def Registeration(request):
    page = 'Registeration'
    Form = MyUserCreationForm()
    group = Group.objects.get(name="guest")
    Emp = Group.objects.get(name="Emp")

    if request.method == "POST":
        Form = MyUserCreationForm(request.POST)
        if Form.is_valid():
            user = Form.save()
            user.groups.add(group)
            
            return redirect("login")
    context = {"page":page,"Form":Form}
    return render(request, "Res/login_register.html", context)



def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        

        try:
            user = User.objects.get(Email=email)
        except:
            messages.error(request, 'user dosnt exist')
        
        user = authenticate(request, Email=email, password = password)
        if user != None:
            login(request, user)
            role = request.user.role
            if role == "Emp":
                return redirect('DashBoard')
            else:
                return redirect('index')
        else:
            messages.error(request, 'username or password are wrong!')

    context = {'page':page}
    return render(request, 'Res/login_register.html' ,context)

def logout_view(request):
    logout(request)
    return redirect('login')

def index(request):
    role = None
    if request.user.is_authenticated:
        role = str(request.user.groups.all()[0])
        if role == 'Emp':
            return redirect('DashBoard')
    context = {'role':role}
    return render(request, 'Res/index.html' ,context)
def menu(request):
    q = request.GET.get('q')
    if q:
        item = Items.objects.get(id=q)
        user = request.user
        order, notcreated = Orders.objects.get_or_create(items = item , user = user) 
        if notcreated == False:
            x = order.quantity 
            x= x+1
            order.quantity = x
            print(x)
            order.save()
            
            return redirect("menu")

    items = Items.objects.all()
    context = {'items':items}
    return render(request, 'Res/menu.html' ,context)

def about(request):
    items = Items.objects.all()
    context = {'items':items}
    return render(request, 'Res/about.html' ,context)

def contact(request):
    if request.method == "POST":
        Contact.objects.create(
            message = request.POST.get('message'),
            user = request.user
            
        )
    context = {}
    return render(request, 'Res/contact.html' ,context)

def reservation(request):
    if request.method == 'POST':
        reservation = Reservation.objects.create(
        user = request.user,
        members = int(request.POST.get('members')),
        table_number = request.POST.get('table_number'),
        Reservation_time = request.POST.get('date'),
        )
        reservation.save()
        

    context = {}
    return render(request, 'Res/reservation.html' ,context)


def stuff(request):
    context = {}
    return render(request, 'Res/stuff.html' ,context)
    
def gallery(request):
    context = {}
    return render(request, 'Res/gallery.html' ,context)

@login_required(login_url='login')
def cart(request):
    user = request.user
    orders = Orders.objects.filter(user__id = user.id)
    total = 0
    for order in orders:
        total = total + (order.items.price * order.quantity)
    if request.method == "POST":
        
        order_id = request.POST.get('order') #send none value
        quantity = request.POST.get('quantity')
        order = Orders.objects.get(id=order_id)
        order.quantity = quantity
        order.save()
        return redirect("cart")


        
    context = {'orders':orders,'total':int(total)}
    return render(request, 'Res/cart.html' ,context)


def blog(request):
    posts = Posts.objects.all()
    context = {'posts':posts}
    return render(request, 'Res/blog.html' ,context)


def blogDetails(request,pk):
    post = Posts.objects.get(id = pk)
    msg = Messages.objects.filter(post = post)
    if request.method=='POST':
        Messages.objects.create(
            body = request.POST.get('message'),
            user = request.user,
            post = post
        )
    context = {'post':post, 'msg':msg}
    return render(request, 'Res/blog-details.html' ,context)


def profile_reservation(request):
    user = request.user 
    Page = 'reservation'
    reservation = Reservation.objects.filter(user__id = user.id)
    context = {'reservation':reservation, 'Page':Page}
    return render(request, 'Res/profile.html' ,context)

def profile_orders(request):
    user = request.user
    Page = 'orders'
    orders = Orders.objects.filter(user__id = user.id)
    context = {'orders':orders,'Page':Page}
    return render(request, 'Res/profile.html' ,context)


def edit_profile(request):
    user = request.user
    Page = 'edit'
    Host = User.objects.get(id=user.id)
    Form = UserForm(instance=Host)
    
    if request.method == 'POST':
        Form = UserForm(request.POST,request.FILES, instance = Host )
        if Form.is_valid():
            Form.save()
            
       
    context = {'Page':Page, 'Form':Form}
    return render(request, 'Res/profile.html' ,context)



def DeleteItem(request,pk):
    order = Orders.objects.get(id=pk)
    role = None
    if request.user.is_authenticated:
        role = str(request.user.groups.all()[0])
    if request.method == "POST":
        order.delete()
        return redirect("cart")
        # quantity = 
    context = {'obj':order.items, "role":role}
    return render(request, 'Res/sure.html' ,context)

def CustomersView(request):
    chart = '1'
    role = None
    if request.user.is_authenticated:
        role = str(request.user.groups.all()[0])
    users = User.objects.all()
    currentmonth = datetime.now().month
    currentyear = datetime.now().year
    users1 = []
    month = int(currentmonth)
    monthlist=[]
    for mo in range (5):
        monthlyusers = User.objects.filter(date_joined__month=month, date_joined__year=currentyear).count()
        users1.append(monthlyusers)
        monthlist.append(month)
        print(monthlist)
        if month == 1 :
            month = 12
            currentyear = currentyear -1
        else:
            month = month - 1 
    print(users1)
        
    context = {
        "users":users,
        "role":role,
        "users1":users1,
        "monthlist":monthlist,
        "chart":chart
        }
    return render(request, 'Res/Customers.html',context)

def CustomersChart2(request):
    chart = '2'
    role = None
    if request.user.is_authenticated:
        role = str(request.user.groups.all()[0])
    users = User.objects.all()
    currentmonth = datetime.now().month
    currentyear = datetime.now().year
    users1 = []
    month = int(currentmonth)
    monthlist=[]
    for mo in range (5):
        monthlyusers = User.objects.filter(date_joined__month=month, date_joined__year=currentyear).count()
        users1.append(monthlyusers)
        monthlist.append(month)
        print(monthlist)
        if month == 1 :
            month = 12
            currentyear = currentyear -1
        else:
            month = month - 1 
    print(users1)
        
    context = {
        "users":users,
        "role":role,
        "users1":users1,
        "monthlist":monthlist,
        "chart":chart
        }
    return render(request, 'Res/Customers.html',context)
def CustomersChart3(request):
    chart = '3'
    role = None
    if request.user.is_authenticated:
        role = str(request.user.groups.all()[0])
    users = User.objects.all()
    currentmonth = datetime.now().month
    currentyear = datetime.now().year
    users1 = []
    month = int(currentmonth)
    monthlist=[]
    for mo in range (5):
        monthlyusers = User.objects.filter(date_joined__month=month, date_joined__year=currentyear).count()
        users1.append(monthlyusers)
        monthlist.append(month)
        print(monthlist)
        if month == 1 :
            month = 12
            currentyear = currentyear -1
        else:
            month = month - 1 
    print(users1)
        
    context = {
        "users":users,
        "role":role,
        "users1":users1,
        "monthlist":monthlist,
        "chart":chart
        }
    return render(request, 'Res/Customers.html',context)

def CustomerDetails(request,pk):
    role = None
    if request.user.is_authenticated:
        role = str(request.user.groups.all()[0])
    user = User.objects.get(id=pk)
    context = {"user":user,"role":role}
    return render(request, 'Res/CustomerDetails.html',context)

def Reservations(request):
    chart = 1
    role = None
    if request.user.is_authenticated:
        role = str(request.user.groups.all()[0])
    Reservations = Reservation.objects.all()
    context = {"Reservations":Reservations,"role":role,"chart":chart}
    return render(request, 'Res/Reservations.html',context)
# def ReservationsChart2(request):
#     chart = 2
#     role = None
#     if request.user.is_authenticated:
#         role = str(request.user.groups.all()[0])
#     Reservations = Reservation.objects.all()
#     context = {"Reservations":Reservations,"role":role,"chart":chart}
#     return render(request, 'Res/Reservations.html',context)

def ReservationDetails(request,pk):
    reservation = Reservation.objects.get(id = pk)
    role = None
    if request.user.is_authenticated:
        role = str(request.user.groups.all()[0])
    
    context = {"Reservation":reservation,"role":role}
    return render(request, 'Res/ReservationDetails.html',context)

def orders(request):
    role = None
    if request.user.is_authenticated:
        role = str(request.user.groups.all()[0])
    orders = Orders.objects.all()
    context = {"orders":orders,"role":role}
    return render(request, 'Res/Orders.html',context)

def OrderDetails(request,pk):
    order = Orders.objects.get(id = pk)
    role = None
    if request.user.is_authenticated:
        role = str(request.user.groups.all()[0])
    
    context = {"order":order,"role":role}
    return render(request, 'Res/OrderDetails.html',context)

def chart(request):
    orders = Orders.objects.all()
    orderitems = []
    for order in orders:
        orderitems.append(order.items.name)
    print(orderitems)
    context = {"orders":orderitems}
    return render(request,"Res/chartjs.html",context)

def DashBoard(request):
    user = request.user
    thisMonth = datetime.now().month
    today = datetime.now().day
    orders = Orders.objects.filter(created__day =today)
    olddailyPrice = 0
    dailyPrice = 0
    for order in orders:
        price = int(order.quantity * order.items.price)
        olddailyPrice = dailyPrice
        dailyPrice = dailyPrice + price
    print(dailyPrice)
    print(olddailyPrice)
    if olddailyPrice == 0 and dailyPrice == 0 :
        percentage = 0
    else : 
        percentage = int(dailyPrice / olddailyPrice  *100 ) -100
    #__________________________________________________________ 
    monthlyorders = Orders.objects.filter(created__month = thisMonth) 
    monthlyPrice = 1
    for order in monthlyorders:
        price = int(order.quantity * order.items.price)
        oldmonthlyPrice = monthlyPrice
        monthlyPrice = monthlyPrice + price
    monthlypercentage = int(monthlyPrice  / oldmonthlyPrice *100) -100
    thismonthcustomers = User.objects.filter(date_joined__month = thisMonth).count()
    lastmonthcustomers = User.objects.filter(date_joined__month = int(thisMonth) - 1).count()
    customerpircentage = int(thismonthcustomers /lastmonthcustomers *100 ) -100
    #__________________________________________________________ 

    todayReservations = Reservation.objects.filter(created__day = today).count()
    yesterdayReservation = Reservation.objects.filter(created__day = today -1).count()
    if yesterdayReservation == 0:
        yesterdayReservation = 1
    Reservationpircentage = int(todayReservations /yesterdayReservation *100 ) -100

    #__________________________________________________________ 

    context = {
    "dailyPrice":dailyPrice,"percentage":percentage
    ,"monthlypercentage":monthlypercentage,"monthlyPrice":monthlyPrice,
    "customerpircentage":customerpircentage,"thismonthcustomers":thismonthcustomers,
    "Reservationpircentage":Reservationpircentage,"todayReservations":todayReservations,"user":user
    }
    return render(request,'Res/DashBoard.html',context)

def ReservationTables(request):
    reservations = Reservation.objects.all()
    print(reservations)
    context = {"reservations":reservations}
    return render(request,'Res/ReservationTables.html',context)

def OrderTables(request):
    orders = Orders.objects.all()

    context = {"orders":orders}
    return render(request,'Res/OrderTables.html',context)

def jstest(request):
    order = Orders.objects.get(id=23)
    return render(request,"static/js/chart.js",{"order":order})