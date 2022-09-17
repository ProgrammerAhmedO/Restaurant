from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import *
from django import forms

class DateTimePickerInput(forms.DateTimeInput):
        input_type = 'datetime'

# class ReservationForm(ModelForm):
#     class Meta:
#         model = Reservation
#         fields = '__all__'


#     def __init__(self, *args, **kwargs):
#         super(ReservationForm, self).__init__(*args, **kwargs)
#         self.fields['members'].widget.attrs.update({'class': 'custom-select d-block form-control'})
#         self.fields['Reservation_time'].widget.attrs.update({'class': 'custom-select d-block form-control'})
#         self.fields['table_number'].widget.attrs.update({'class': 'custom-select d-block form-control'})

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['Email','phone_number','location','first_name','last_name','pic']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        # self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['Email'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control'})
        self.fields['location'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['pic'].widget.attrs.update({'class': 'form-control', 'value':'update you pic'})

class OrdersForm(ModelForm):
    class Meta:
        model = Orders
        fields = ['quantity']
    def __init__(self, *args, **kwargs):
        super(OrdersForm, self).__init__(*args, **kwargs)

        self.fields['quantity'].widget.attrs.update({'class': 'form-control'})

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
    def __init__(self, *args, **kwargs):
        super(MyUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control','placeholder':'username'})
        self.fields['email'].widget.attrs.update({'class': 'form-control','placeholder':'Email'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control','placeholder':'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control','placeholder':'Confirm Password'})