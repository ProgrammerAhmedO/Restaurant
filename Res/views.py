from datetime import datetime
from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
import speech_recognition as sr #ML
from django.db.models import Q
from geopy.geocoders import Nominatim
import operator
import stripe
from django.conf import settings
from django.http import JsonResponse
from flask import Flask



#Registeration/Login and Logout_______________________________________________
def Registeration(request):
    page = 'Registeration'
    Form = MyUserCreationForm()
    group = Group.objects.get(name="guest")
    Emp = Group.objects.get(name="Emp")

    if request.method == "POST":
        Form = MyUserCreationForm(request.POST)
        if Form.is_valid():
            print("gg")
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
        email = request.POST.get('Email')
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


#Customer View _________________________________________
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


# Profile View 
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


# Admin Part ________________________________________________________________________
# Chart Pages 
def OrderCharts(request):
    ListItems = ToDoList.objects.filter(user=request.user)
    ordersCounter = Orders.objects.all().count()
    items = Items.objects.all()
    orderItems = []
    orderData = []
    for item in items:
        orderItems.append(item.name)
        orderData.append( Orders.objects.filter(items__name = item.name).count())
    print(orderItems)
    print(orderData)
    #_____________________________________________________
    #search part 
    if request.method == "POST":
        search = request.POST.get("search")
        if search != None:
            if search.capitalize() == "Order" or search.capitalize() == "Orders":
                return redirect("OrderTables")
            elif search.capitalize() == "Reservation" or search.capitalize() == "Reservations":
                return redirect("ReservationTables")
            elif search.capitalize() == "Customer" or search.capitalize() == "Customer" or search.capitalize() == "User" or search.capitalize() == "Users":
                return redirect("OrderTables")
            elif search.capitalize() == "Graph" or search.capitalize() == "Graphs" or search.capitalize() == "Chart" or search.capitalize() == "Charts":
                return redirect("OrderCharts")
            else:
                return redirect("DashBoard")
    #_____________________________________________________

    context = {
    "orderItems":orderItems,
    "orderData":orderData , 
    "ordersCounter":ordersCounter,
    "ListItems":ListItems}
    return render(request,"Res/Charts/OrderCharts.html",context)
def CustomerCharts(request):
    ListItems = ToDoList.objects.filter(user=request.user)
    AllUsers = User.objects.all().count()
    currentmonth = datetime.now().month
    monthes = []
    monthlyUsers = []
    for i in range(4,-1,-1):
        monthes.append(currentmonth - i)
        monthlyUsers.append(User.objects.filter(date_joined__month = monthes[len(monthes) -1]).count())
    print(monthes)
    print(monthlyUsers)
    #_____________________________________________________
    #search part 
    if request.method == "POST":
        search = request.POST.get("search")
        if search != None:
            if search.capitalize() == "Order" or search.capitalize() == "Orders":
                return redirect("OrderTables")
            elif search.capitalize() == "Reservation" or search.capitalize() == "Reservations":
                return redirect("ReservationTables")
            elif search.capitalize() == "Customer" or search.capitalize() == "Customer" or search.capitalize() == "User" or search.capitalize() == "Users":
                return redirect("OrderTables")
            elif search.capitalize() == "Graph" or search.capitalize() == "Graphs" or search.capitalize() == "Chart" or search.capitalize() == "Charts":
                return redirect("OrderCharts")
            else:
                return redirect("DashBoard")
    #_____________________________________________________
    context = {"monthes":monthes,"monthlyUsers":monthlyUsers
    ,"ListItems":ListItems , "AllUsers":AllUsers}
    return render(request,"Res/Charts/CustomerCharts.html",context)
def ReservationCharts(request):
    ListItems = ToDoList.objects.filter(user=request.user)
    AllReservations = Reservation.objects.all().count()
    currentmonth = datetime.now().month
    monthes = []
    monthlyReservations = []
    for i in range(4,-1,-1):
        monthes.append(currentmonth - i)
        monthlyReservations.append(Reservation.objects.filter(created__month = monthes[len(monthes) -1]).count())
    print(monthes)
    print(monthlyReservations)
        #_____________________________________________________
    #search part 
    if request.method == "POST":
        search = request.POST.get("search")
        if search != None:
            if search.capitalize() == "Order" or search.capitalize() == "Orders":
                return redirect("OrderTables")
            elif search.capitalize() == "Reservation" or search.capitalize() == "Reservations":
                return redirect("ReservationTables")
            elif search.capitalize() == "Customer" or search.capitalize() == "Customer" or search.capitalize() == "User" or search.capitalize() == "Users":
                return redirect("OrderTables")
            elif search.capitalize() == "Graph" or search.capitalize() == "Graphs" or search.capitalize() == "Chart" or search.capitalize() == "Charts":
                return redirect("OrderCharts")
            else:
                return redirect("DashBoard")
    #_____________________________________________________

    context = {"monthes":monthes,"monthlyUsers":monthlyReservations 
    ,"ListItems":ListItems, "AllReservations":AllReservations}
    return render(request,"Res/Charts/CustomerCharts.html",context)


#DashBoard
@login_required(login_url='login')
def DashBoard(request):
    user = request.user
    # print(user)
    role = str(user.groups.all()[0])
    # print(role)
    if role != 'Emp':
        return redirect('index')
    else:
    #_____________________________________________________
    #search part 
        if request.method == "POST":
            search = request.POST.get("search")
            if search != None:
                if search.capitalize() == "Order" or search.capitalize() == "Orders":
                    return redirect("OrderTables")
                elif search.capitalize() == "Reservation" or search.capitalize() == "Reservations":
                    return redirect("ReservationTables")
                elif search.capitalize() == "Customer" or search.capitalize() == "Customer" or search.capitalize() == "User" or search.capitalize() == "Users":
                    return redirect("OrderTables")
                elif search.capitalize() == "Graph" or search.capitalize() == "Graphs" or search.capitalize() == "Chart" or search.capitalize() == "Charts":
                    return redirect("OrderCharts")
                else:
                    return redirect("DashBoard")
    #_____________________________________________________
    #best item :
        users = User.objects.all()
        usersFavoritItmeList = []
        for user in users :
            usersFavoritItmeList.append(user.FavoriteFood())

        mostorder =  max(((item, usersFavoritItmeList.count(item)) for item in set(usersFavoritItmeList)), key=lambda a: a[1])[0]

        BestItem = Items.objects.get(name=mostorder)
    #_____________________________________________________
    #Messages From Post
        posts = Posts.objects.filter(user = request.user)
        message = []
        msgCounter = -1
        for post in posts:
            message = (post.AllMessages())
            msgCounter = msgCounter + post.AllMessages().count()

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
        #manage todo list
        ##add list item
        todo = None
        ListItems = ToDoList.objects.filter(user=request.user)
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
        # print(ListOfItems)
        for item in ListOfItems:
            ordersNumber = Orders.objects.filter(items__name=item).count()
            ordersCount.append(ordersNumber)
        # print(ordersCount)
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
            # print(userorders)
            for order in userorders:
                # print("the order is :",order)
                orderprice = order.total_price()
                totalprice = totalprice + orderprice
            ordersPricelist.append(totalprice)
            userlist.append(user.id)
            UserListCount = UserListCount + 1
            totalprice = 0
        # print("ordersPricelist",ordersPricelist)
        # print("list of users",userlist)
        # print("number of total users",UserListCount)
        # sortedlist = sorted(BestOrdersPrice, key=abs , reverse=True)
        index = 0
        bestuser = 1
        bestuserslist = []
        BestOrdersPriceList = []
        BestOrdersPrice = 0
        for i in range(UserListCount):
            BestOrdersPrice = 0
            # print("i=",i)
            for number in range(len(ordersPricelist) ):
                # print("number=", number)
                if int(ordersPricelist[number]) > BestOrdersPrice:
                    bestuser = User.objects.get(id= userlist[number])
                    BestOrdersPrice = ordersPricelist[number]
                    index = number 
            # print("index:",index)
            ordersPricelist.remove(ordersPricelist[index])
            userlist.remove(userlist[index])
            bestuserslist.append(bestuser)
            BestOrdersPriceList.append(BestOrdersPrice)
            index = 0
            # print("out of loop:","users list",bestuserslist,"price list",BestOrdersPriceList)
            



        # print( "best users list ", bestuserslist)
        # print("best orders list",BestOrdersPriceList)
            
        #__________________________________________________________ 
        # Voice assistant part
        # if request.method == "POST":
        #     listener = sr.Recognizer()
        #     try:
        #             print("listining")
        #             voice = listener.listen(sr.Microphone())
        #             command = listener.recognize_google(voice)
        #             print(command)
        #     except:
        #         pass
        #__________________________________________________________ 
        # location Part

        countriesList = []
        users = User.objects.all()
        for user in users:
            country = user.UserCounty()
            if country != None:
                countriesList.append(country)
        countriesSet = set(countriesList)
        uniqueCountryList = list(countriesSet)
        
        UsersInCountry = []
        for i in range(len(uniqueCountryList)):
            UsersInCountry.append(operator.countOf(countriesList,uniqueCountryList[i]))
        #uniqueCountryList the country 
        #UsersInCountry the number of users in each country
        #UsersInCountryPercintage the percintage of each country 
        UsersInCountryPercintage = []
        for i in UsersInCountry:
            UsersInCountryPercintage.append(i/sum(UsersInCountry)*100)
        print(uniqueCountryList)
        print(UsersInCountry)
        print(UsersInCountryPercintage)


        #__________________________________________________________ 
        context = {
        "dailyPrice":dailyPrice,"percentage":percentage,
        "todayorders":todayorders,"uniqueCountryList":uniqueCountryList,
        "todayuserjoined":todayuserjoined,"UsersInCountry":UsersInCountry,
        "todayuserspercentage":todayuserspercentage,
        "orderspercentage":orderspercentage,
        "monthlypercentage":monthlypercentage,
        "monthlyPrice":monthlyPrice,"BestItem":BestItem,
        "customerpircentage":customerpircentage,"msgCounter":msgCounter,
        "thismonthcustomers":thismonthcustomers,
        "thismonthReservations":thismonthReservations,
        "monthlyReservationPercentage":monthlyReservationPercentage,
        "Reservationpircentage":Reservationpircentage,
        "todayReservations":todayReservations,"user":request.user,
        "reservations":reservations,"ListItems":ListItems[0:5],"index":index,
        "contacts":contacts[0:4],"items":items,"message":message,
        "ListOfItems":ListOfItems,"bestuser":bestuser,"BestOrdersPrice":BestOrdersPrice,
        "bestuserslist":bestuserslist,"BestOrdersPriceList":BestOrdersPriceList,
        }
        return render(request,'Res/DashBoard.html',context)

# Table Pages
@login_required(login_url='login')
def ReservationTables(request):
    reservations = Reservation.objects.all()
    if request.method == "POST":
        search = request.POST.get("search")
        if search != None :
            reservations = Reservation.objects.filter(Q(user__name__icontains=search) | Q(user__Email__icontains=search) |Q(members__icontains=search)|Q(Reservation_time__icontains=search))
    context = {"reservations":reservations}
    return render(request,'Res/Tables/ReservationTables.html',context)
@login_required(login_url='login')
def OrderTables(request):
    orders = Orders.objects.all()
    # users = User.objects.all()
    # userTotalPriceList = []
    # UserList = []

    # TotalPrice = 0
    # for user in users:
    #     userorders = Orders.objects.filter(user=user)
    #     print(userorders)
    #     for price in userorders:
    #         TotalPrice = TotalPrice + price.total_price()
    #     UserList.append(user)
    #     userTotalPriceList.append(TotalPrice)
    #     TotalPrice = 0
    if request.method == "POST":
        search = request.POST.get("search")
        if search != None :
            orders = Orders.objects.filter(Q(user__name__icontains=search) | Q(user__Email__icontains=search) |Q(items__name__icontains=search)|Q(created__icontains=search)|Q(quantity__icontains=search))

    context = {"orders":orders,} #"UserList":UserList,"userTotalPriceList":userTotalPriceList,
    return render(request,'Res/Tables/OrderTables.html',context)
@login_required(login_url='login')
def CustomerTables(request):
    users = User.objects.all()
    if request.method == "POST":
        search = request.POST.get("search")
        if search != None :
            users = User.objects.filter(Q(name__icontains=search) | Q(Email__icontains=search) |Q(phone_number__icontains=search)|Q(date_joined__icontains=search)|Q(orders__id__icontains=search))

    context = {"users":users}
    return render(request,'Res/Tables/CustomerTables.html',context)



# Stripe Payment Method
stripe.api_key = settings.STRIPE_SECRET_KEY
app = Flask(__name__,
            static_url_path='',
            static_folder='public')
YOUR_DOMAIN = 'http://localhost:8000'

@login_required(login_url='login')
@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session(request):

    user = request.user
    Total_Orders = orders = Orders.objects.filter(user__id = user.id).count()
    orders = Orders.objects.filter(user__id = user.id)
    total = 0
    for order in orders:
        total = total + (order.items.price * order.quantity)
    total_to_pay = int(total *100)


    product = stripe.Product.create(
    name=f'Total of {Total_Orders} Order/s with amount of :',
    description='thx for using our service ',
    images=['https://img.freepik.com/premium-vector/vector-shopping-cart-icon-paper-sticker-with-shadow-colored-shopping-symbol-isolated_118339-1774.jpg?w=2000'],
    )

    price = stripe.Price.create(
    product=product.id,
    unit_amount=total_to_pay,
    currency='usd',
    )
    try:
        checkout_session = stripe.checkout.Session.create(

            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': price.id,
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/cart/',
         
        )
        return redirect(checkout_session.url)
    except Exception as e:
            return JsonResponse({'error': str(e)})
    
if __name__ == '__main__':
    app.run(port=8000)

@login_required(login_url='login')
def success(request):
    return render (request, 'Res/Payment/success.html')