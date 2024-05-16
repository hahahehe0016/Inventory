from dataclasses import fields
from django import forms 
from .models import Order, Product, Employee, Component, Allocation
from django.forms import DateField, widgets


class DateInput(forms.DateInput):
    input_type = 'date'

class ProductForm(forms.ModelForm):

    remarks = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '', 'style': 'height: 100px;' 'width: 860px', 'class': 'form-control'}), required=False)
    
    class Meta:
        model = Product
        widgets = {
            'date': DateInput(),
        }
        fields = ['model_name', 'asset_type','department', 'serial_number', 'OR_number','supplier_name', 'status', 'date', 'remarks', 'asset_image','site']

class ProcurementForm(forms.ModelForm):

    #remarks = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '', 'style': 'height: 100px;', 'class': 'form-control'}))
    
    class Meta:
        model = Product
        widgets = {
            'date': DateInput(),
        }
        fields = ['model_name', 'asset_type', 'serial_number' ]


class OrderForm(forms.ModelForm):

    disposal_remarks = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '', 'style': 'height: 90px;', 'class': 'form-control'}))

    class Meta:
        model = Order
        fields = ['product', 'disposal_remarks', 'person_in_charge']

class EmployeeForm(forms.ModelForm):

    in_name = forms.CharField(label='First Name')
    out_name = forms.CharField(label='Last Name')
    emp_email = forms.CharField(label='Employee Email')

    class Meta:
        model = Employee
        fields = ['in_name', 'out_name', 'emp_email', 'emp_department']

class ComponentForm(forms.ModelForm):
    
    class Meta:
        widgets = {
            'date_installed': DateInput(),
            'date_replaced': DateInput(),
        }
        model = Component
        fields = ['date_installed', 'date_replaced', 'activeness', 'motherboard', 'processor', 'gpu', 'RAM1', 'RAM2', 'RAM3', 'RAM4', 'PSU', 'HDD1', 'HDD2', 'HDD3', 'HDD4', 'Others']

class AllocationForm(forms.ModelForm):

    class Meta:
        model = Allocation
        fields = ['allocation_employee', 'location', 'asset_allocation', 'system_allocation']

