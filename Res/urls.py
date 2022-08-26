from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index , name ='index'),
    path('menu', views.menu , name ='menu'),
    path('about', views.about , name ='about'),
    path('contact', views.contact , name ='contact'),
    path('reservation', views.reservation , name ='reservation'),
    path('stuff', views.stuff , name ='stuff'),
    path('gallery', views.gallery , name ='gallery'),
    path('blog-details/<str:pk>', views.blogDetails , name ='blog-details'),
    path('blog', views.blog , name ='blog'),
    path('login', views.loginPage , name ='login'),
    path('logout', views.logout_view , name ='logout'),
    path('profile_reservation/', views.profile_reservation , name ='profile_reservation'),
    path('profile_orders/', views.profile_orders , name ='profile_orders'),
    path('edit_profile/', views.edit_profile , name ='edit_profile'),
    path('cart/', views.cart , name ='cart'),
    path('Registeration/', views.Registeration , name ='Registeration'),
    path('DeleteItem/<str:pk>', views.DeleteItem , name ='DeleteItem'),
    path('DeleteItem/<str:pk>', views.DeleteItem , name ='DeleteItem'),
    path('Customers/', views.CustomersView , name ='Customers'),
    path('CustomersChart2/', views.CustomersChart2 , name ='CustomersChart2'),
    path('CustomersChart3/', views.CustomersChart3 , name ='CustomersChart3'),
    path('CustomerDetails/<str:pk>/', views.CustomerDetails , name ='CustomerDetails'),
    path('Reservations/', views.Reservations , name ='Reservations'),
    # path('ReservationsChart2/', views.ReservationsChart2 , name ='ReservationsChart2'),
    path('ReservationDetails/<str:pk>/', views.ReservationDetails , name ='ReservationDetails'),
    path('orders/', views.orders , name ='orders'),
    path('OrderDetails/<str:pk>/', views.OrderDetails , name ='OrderDetails'),
    path('chart/', views.chart , name ='chart'),
    path('DashBoard/', views.DashBoard , name ='DashBoard'),
    path('ReservationTables/', views.ReservationTables , name ='ReservationTables'),
    path('OrderTables/', views.OrderTables , name ='OrderTables'),


    
    

]
