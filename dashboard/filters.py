from sqlite3 import Date
from .models import *
from django import forms
from django.forms import DateInput, widgets
import django_filters
from django_filters.widgets import RangeWidget


class ProductFilter(django_filters.FilterSet):

    #date_range = django_filters.DateFromToRangeFilter(field_name='date')
    #date_range = django_filters.DateRangeFilter(field_name='date')
    date = django_filters.DateFromToRangeFilter(widget=RangeWidget(attrs={'type' : 'date'}))
    #date = django_filters.DateFilter(widget=DateInput(attrs={'type': 'date'}))
    po = django_filters.CharFilter(label='Purchase Order #')

    class Meta:
        model = Product
        fields = ['po','model_name','asset_type','serial_number', 'OR_number', 'department', 'status', 'date',]

class AssetFilter(django_filters.FilterSet):

    class Meta:
        model = Product
        fields = ['model_name','asset_type','serial_number', 'OR_number', 'department', 'status', 'date',]


class EmployeeFilter(django_filters.FilterSet):

    in_name = django_filters.CharFilter(label = 'First Name')
    out_name = django_filters.CharFilter(label = 'Last Name')
    emp_email = django_filters.CharFilter(label = 'Email')

    class Meta:
        model = Employee
        fields = ['in_name','out_name','emp_email', 'emp_department',]

class AllocationFilter(django_filters.FilterSet):

    alloc_date = django_filters.DateFromToRangeFilter(widget=RangeWidget(attrs={'type' : 'date'}))

    class Meta:
        model = Allocation
        fields = ['allocation_employee','location','asset_allocation','system_allocation', 'alloc_date']


class ComponentFilter(django_filters.FilterSet):

    class Meta:
        model = Component
        fields = ['compo_name','activeness','motherboard','processor', 'gpu', 'RAM1', 'RAM2', 'RAM3', 'RAM4', 'PSU', 'HDD1', 'HDD2', 'HDD3', 'HDD4', 'Others']

