from datetime import datetime
from multiprocessing import context
from os import remove
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

        if month == 1 :
            month = 12
            currentyear = currentyear -1
        else:
            month = month - 1 

        
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

        if month == 1 :
            month = 12
            currentyear = currentyear -1
        else:
            month = month - 1 

        
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

        if month == 1 :
            month = 12
            currentyear = currentyear -1
        else:
            month = month - 1 

        
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

    context = {"orders":orderitems}
    return render(request,"Res/chartjs.html",context)


@login_required(login_url='login')
def DashBoard(request):
    user = request.user
    print(user)
    role = str(user.groups.all()[0])
    print(role)
    if role != 'Emp':
        return redirect('index')
    else:
    #_____________________________________________________

        thisMonth = datetime.now().month
        today = datetime.now().day
        orders = Orders.objects.filter(created__day =today)
        olddailyPrice = 0
        dailyPrice = 0
        for order in orders:
            price = int(order.quantity * order.items.price)
            olddailyPrice = dailyPrice
            dailyPrice = dailyPrice + price


        if olddailyPrice == 0 and dailyPrice == 0 :
            percentage = 0
        elif olddailyPrice == 0 and dailyPrice != 0 :
            olddailyPrice = 1
            percentage = int(dailyPrice / olddailyPrice  *100 ) -100
        else : 
            percentage = int(dailyPrice / olddailyPrice  *100 ) -100
        #__________________________________________________________ 
        monthlyorders = Orders.objects.filter(created__month = thisMonth) 
        monthlyPrice = 1
        oldmonthlyPrice = 1
        for order in monthlyorders:
            price = int(order.quantity * order.items.price)
            oldmonthlyPrice = monthlyPrice
            monthlyPrice = monthlyPrice + price
        monthlypercentage = int(monthlyPrice  / oldmonthlyPrice *100) -100
        thismonthcustomers = User.objects.filter(date_joined__month = thisMonth).count()
        lastmonthcustomers = User.objects.filter(date_joined__month = int(thisMonth) - 1).count()
        customerpircentage = int(thismonthcustomers /lastmonthcustomers *100 ) -100
        thismonthReservations = Reservation.objects.filter(created__month = thisMonth).count()
        lastmonthReservations = Reservation.objects.filter(created__month = thisMonth -1).count()
        if lastmonthReservations == 0:
            lastmonthReservations = 1
        monthlyReservationPercentage = int(thismonthReservations /lastmonthReservations *100 ) -100
        todayorders = Orders.objects.filter(created__day = today).count()
        lastdayorders = Orders.objects.filter(created__day = today -1 ).count()
        if lastdayorders == 0 :
            lastdayorders = 1
        orderspercentage = int(todayorders /lastdayorders *100 ) -100
        todayuserjoined = User.objects.filter(date_joined__day = today).count()
        lastdayuserjoined = User.objects.filter(date_joined__day = today -1 ).count()
        if lastdayuserjoined == 0 :
            lastdayuserjoined = 1
        todayuserspercentage = int(todayuserjoined /lastdayuserjoined *100 ) -100
        #__________________________________________________________ 
        #passen data
        reservations = Reservation.objects.all()
        #__________________________________________________________ 

        todayReservations = Reservation.objects.filter(created__day = today).count()
        yesterdayReservation = Reservation.objects.filter(created__day = today -1).count()
        if yesterdayReservation == 0:
            yesterdayReservation = 1
        Reservationpircentage = int(todayReservations /yesterdayReservation *100 ) -100

        #__________________________________________________________ 
        q = None
        if request.method == "POST":
            q = request.POST.get('search')
            if q is not None:
                if q.capitalize() == 'Dashboard' or q.capitalize()  == 'Board':
                    return redirect ('DashBoard')
                elif q.capitalize() == 'Chart' or q.capitalize() == 'Graph' :
                    return redirect ('chart')
                elif q.capitalize() == 'Reservation' or q.capitalize() == 'Reservations' :
                    return redirect ('ReservationTables')

        #__________________________________________________________ 
        #manage todo list
        ##add list item
        todo = None
        ListItems = ToDoList.objects.filter(user=user)
        if request.method == "POST":
            todo = request.POST.get('todo')
            if todo != None and todo != "":
                # checkbox = request.POST.get('checkbox')
                # print(checkbox)
                ToDoList.objects.create(
                    user = request.user,
                    body = todo
                )
                return redirect("DashBoard")
            todo = None
        # manage delete item

        itemid = request.GET.get('q')
        if itemid is not None:
            item,Notcreated = ToDoList.objects.get_or_create(id=itemid, user=request.user)
            if Notcreated == False:
                item.delete()
            elif Notcreated == True:
                item.delete()

        #__________________________________________________________ 
        #User contact part
        contacts = Contact.objects.all()

        #__________________________________________________________ 
        #Items part
        items = Items.objects.all()
        ordersCount = []
        ListOfItems = []
        for item in items:
            ListOfItems.append(item)
        print(ListOfItems)
        for item in ListOfItems:
            ordersNumber = Orders.objects.filter(items__name=item).count()
            ordersCount.append(ordersNumber)
        print(ordersCount)
        specificuser = User.objects.get(id=1)
        #read more about location attributes
        specificuserCuntry = specificuser.location
        # print(specificuserCuntry)
        #__________________________________________________________ 
        #top users
        ordersPricelist = []
        userlist = []
        totalprice = 0
        users = User.objects.all()
        UserListCount = 0
        for user in users:
            userorders = Orders.objects.filter(user__id = user.id)
            print(userorders)
            for order in userorders:
                print("the order is :",order)
                orderprice = order.total_price()
                totalprice = totalprice + orderprice
            ordersPricelist.append(totalprice)
            userlist.append(user.id)
            UserListCount = UserListCount + 1
            totalprice = 0
        print("ordersPricelist",ordersPricelist)
        print("list of users",userlist)
        print("number of total users",UserListCount)
        # sortedlist = sorted(BestOrdersPrice, key=abs , reverse=True)
        index = 0
        bestuser = 1
        bestuserslist = []
        BestOrdersPriceList = []
        BestOrdersPrice = 0
        for i in range(UserListCount):
            BestOrdersPrice = 0
            print("i=",i)
            for number in range(len(ordersPricelist) ):
                print("number=", number)
                if int(ordersPricelist[number]) > BestOrdersPrice:
                    bestuser = User.objects.get(id= userlist[number])
                    BestOrdersPrice = ordersPricelist[number]
                    index = number 
            print("index:",index)
            ordersPricelist.remove(ordersPricelist[index])
            userlist.remove(userlist[index])
            bestuserslist.append(bestuser)
            BestOrdersPriceList.append(BestOrdersPrice)
            index = 0
            print("out of loop:","users list",bestuserslist,"price list",BestOrdersPriceList)
            



        print( "best users list ", bestuserslist)
        print("best orders list",BestOrdersPriceList)
            
        #__________________________________________________________ 
        

        context = {
        "dailyPrice":dailyPrice,"percentage":percentage,
        "todayorders":todayorders,
        "todayuserjoined":todayuserjoined,
        "todayuserspercentage":todayuserspercentage,
        "orderspercentage":orderspercentage,
        "monthlypercentage":monthlypercentage,"monthlyPrice":monthlyPrice,
        "customerpircentage":customerpircentage,
        "thismonthcustomers":thismonthcustomers,
        "thismonthReservations":thismonthReservations,
        "monthlyReservationPercentage":monthlyReservationPercentage,
        "Reservationpircentage":Reservationpircentage,
        "todayReservations":todayReservations,"user":request.user,
        "reservations":reservations,"ListItems":ListItems,
        "contacts":contacts,"items":items,
        "ListOfItems":ListOfItems,"bestuser":bestuser,"BestOrdersPrice":BestOrdersPrice,
        "bestuserslist":bestuserslist,"BestOrdersPriceList":BestOrdersPriceList,
        }
        return render(request,'Res/DashBoard.html',context)

def ReservationTables(request):
    reservations = Reservation.objects.all()

    context = {"reservations":reservations}
    return render(request,'Res/ReservationTables.html',context)

def OrderTables(request):
    orders = Orders.objects.all()

    context = {"orders":orders}
    return render(request,'Res/OrderTables.html',context)

def jstest(request):
    order = Orders.objects.get(id=23)
    return render(request,"static/js/chart.js",{"order":order})