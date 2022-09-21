
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
    path('OrderCharts/', views.OrderCharts , name ='OrderCharts'),
    path('CustomerCharts/', views.CustomerCharts , name ='CustomerCharts'),
    path('ReservationCharts/', views.ReservationCharts , name ='ReservationCharts'),
    path('DashBoard/', views.DashBoard , name ='DashBoard'),
    path('ReservationTables/', views.ReservationTables , name ='ReservationTables'),
    path('OrderTables/', views.OrderTables , name ='OrderTables'),
    path('CustomerTables/', views.CustomerTables , name ='CustomerTables'),
    path('create-checkout-session/',views.create_checkout_session , name="create-checkout-session"),
    path('success/',views.success , name="success"),
    path('test/',views.test , name="test"),


    
    

]
