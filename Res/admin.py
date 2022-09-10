# from django.contrib import admin
# from .models import *

# admin.site.register(ToDoList)
# admin.site.register(User)
# admin.site.register(Items)
# admin.site.register(Orders)
# admin.site.register(Reservation)
# admin.site.register(Posts)
# admin.site.register(Messages)
# admin.site.register(Contact)

from django.contrib import admin

from .models import User, Items, Orders, Reservation, Posts, Messages, Contact, ToDoList


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'password',
        'last_login',
        'is_superuser',
        'username',
        'first_name',
        'last_name',
        'email',
        'is_staff',
        'is_active',
        'date_joined',
        'pic',
        'Email',
        'name',
        'location',
        'phone_number',
    )
    list_filter = (
        'last_login',
        'is_superuser',
        'is_staff',
        'is_active',
        'date_joined',
    )
    raw_id_fields = ('groups', 'user_permissions')
    search_fields = ('name',)


@admin.register(Items)
class ItemsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'image',
        'quantity',
        'description',
        'price',
        'type',
    )
    search_fields = ('name',)


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created',
        'items',
        'user',
        'more_information',
        'quantity',
    )
    list_filter = ('created', 'items', 'user')


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created',
        'user',
        'members',
        'table_number',
        'Reservation_time',
    )
    list_filter = ('created', 'user')


@admin.register(Posts)
class PostsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'body', 'user', 'created', 'tag', 'pic')
    list_filter = ('user', 'created')


@admin.register(Messages)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'user', 'created', 'body')
    list_filter = ('post', 'user', 'created')


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'message', 'user', 'created')
    list_filter = ('user', 'created')


@admin.register(ToDoList)
class ToDoListAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'body', 'compeleted', 'user')
    list_filter = ('created', 'compeleted', 'user')

