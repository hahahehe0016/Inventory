from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product
from django.contrib.auth.decorators import login_required
from .models import Product, Order, Employee, Component, Allocation, Disposal
from .forms import ProductForm, OrderForm, EmployeeForm, ProcurementForm, ComponentForm, AllocationForm
from django.contrib.auth.models import User
from django.contrib import messages
from .filters import ProductFilter, EmployeeFilter, AllocationFilter, ComponentFilter
from django.core.paginator import Paginator
from datetime import datetime
import dateutil.relativedelta
import datetime

from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

import xlwt
from django.http import HttpResponse
from django.contrib.auth.models import User
from dashboard.models import Product

from .resources import EmployeeResource
from tablib import Dataset

import csv

# Create your views here.


@login_required(login_url='user-login')
def index(request):
    orders = Order.objects.all()
    products = Product.objects.all()
    not_working = Product.objects.filter(status="Not Working").count()
    no_images = Product.objects.filter(asset_image="Product_Default.png").count()
    no_sn = Product.objects.filter(serial_number=None).count()
    no_or = Product.objects.filter(OR_number=None).count()
    orders_count = orders.count()
    products_count = products.count()
    workers_count = User.objects.all().count()
    employee_count = Employee.objects.all().count()
    format = "%Y-%m-%d"
    now = datetime.date.today() #current time
    now_f = now.strftime(format)
    now_what= now + dateutil.relativedelta.relativedelta(months=-1) #last month
    now_what_f = now_what.strftime(format)
    last_month = Product.objects.filter(date__range=[now_what, now]).count()
    

    if request.method=='POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.employee = request.user
            instance.save()
            return redirect('dashboard-index')
    else:
        form = OrderForm()
    context={
        'orders': orders,
        'form': form,
        'products': products,
        'employee_count': employee_count,
        'orders_count': orders_count,
        'products_count': products_count,
        'workers_count': workers_count,
        'not_working': not_working,
        'no_images': no_images,
        'no_sn': no_sn,
        'no_or': no_or,
        'last_month': last_month,
    }
    return render(request, 'dashboard/index.html', context)

@login_required(login_url='user-login')
def employee(request):
    workers = User.objects.all()
    workers_count = workers.count()
    orders_count = Order.objects.all().count()
    products_count = Product.objects.all().count()
    context ={
        'workers': workers,
        'workers_count': workers_count,
        'orders_count': orders_count,
        'products_count': products_count,
    }
    return render(request, 'dashboard/employee.html', context)

@login_required(login_url='user-login')
def employee1(request):
    workers = User.objects.all()
    workers_count = workers.count()
    orders_count = Order.objects.all().count()
    products_count = Product.objects.all().count()
    context ={
        'workers': workers,
        'workers_count': workers_count,
        'orders_count': orders_count,
        'products_count': products_count,
    }
    return render(request, 'dashboard/employee1.html', context)

@login_required(login_url='user-login')
def employee_detail(request, pk):
    workers = User.objects.get(id=pk)
    workers_count = User.objects.all().count()
    orders_count = Order.objects.all().count()
    products_count = Product.objects.all().count()
    context = {
        'workers' : workers,
        'workers_count': workers_count,
        'orders_count': orders_count,
        'products_count': products_count,
    }
    return render(request, 'dashboard/employee_detail.html', context)

@login_required(login_url='user-login')
def product(request):
    # if 'q' in request.GET:
    #     q = request.GET['q']
    #     items = Product.objects.filter(serial_number__icontains=q)
    #     print(q)
    # else:
    items = Product.objects.all()

    #Using ORM
    #items = Product.objects.all().order_by('-date') #Using ORM
    products_count = items.count()
    #items = Product.objects.raw('SELECT * FROM dashboard_product')
    workers_count = User.objects.all().count
    orders_count = Order.objects.all().count

    myFilter = ProductFilter(request.GET, queryset=items)

    items = myFilter.qs

    p = Paginator(items, 50)

    page_num = request.GET.get('page', 1)

    #print(p.num_pages) #printing total number of pages

    page = p.page(page_num)

    page_obj = p.get_page(page_num)

    item_range = ((p.num_pages - 1) * 50) + 1
    item_range2 = p.num_pages*50

    #print(page_obj.number) #printing the current page

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        form1 = ComponentForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.adder = request.user
            instance.po = " "
            if instance.asset_type == "Hard Disk Drive":
                instance.classification = "001"
            elif instance.asset_type == "Solid State Drive":
                instance.classification = "002"
            elif instance.asset_type == "Graphics Card":
                instance.classification = "003"
            elif instance.asset_type == "Laptop":
                instance.classification = "004"
            elif instance.asset_type == "RAM":
                instance.classification = "005"    
            elif instance.asset_type == "Charger":
                instance.classification = "006"
            elif instance.asset_type == "UPS":
                instance.classification = "007"
            elif instance.asset_type == "Mouse":
                instance.classification = "008"
            elif instance.asset_type == "Keyboard":
                instance.classification = "009"
            elif instance.asset_type == "Motherboard":
                instance.classification = "010"
            elif instance.asset_type == "Monitor":
                instance.classification = "011"
            elif instance.asset_type == "Power Supply":
                instance.classification = "012"
            elif instance.asset_type == "Router":
                instance.classification = "013"
            elif instance.asset_type == "AVR":
                instance.classification = "014"
            elif instance.asset_type == "Tablet":
                instance.classification = "015"
            elif instance.asset_type == "System Unit":
                instance.classification = "016"
            elif instance.asset_type == "Audio Devices":
                instance.classification = "017"
            elif instance.asset_type == "CPU":
                instance.classification = "018"
            else:
                instance.classification = "019"
            instance.save()
            
            product_name = form.cleaned_data.get('model_name')
            image_url = form.cleaned_data.get('asset_image.url')
            messages.success(request, f'{product_name} has been added.')
            return redirect('dashboard-product')
    else:
        form = ProductForm()

    context = {
        'page_object': page_obj,
        'p': p,
        'items': page,
        'form': form,
        'workers_count': workers_count,
        'orders_count': orders_count,
        'products_count': products_count,
        'myFilter': myFilter,
        'item_range': item_range,
        'item_range2': item_range2,
    };
    return render(request, 'dashboard/product.html', context)

@login_required(login_url='user-login')
def product1(request):
    global items
    items = Product.objects.all() #Using ORM
    #items = Product.objects.all().order_by('-date') #Using ORM
    products_count = items.count()
    #items = Product.objects.raw('SELECT * FROM dashboard_product')
    workers_count = User.objects.all().count
    orders_count = Order.objects.all().count

    myFilter = ProductFilter(request.GET, queryset=items)

    items = myFilter.qs

    p = Paginator(items, 10)

    page_num = request.GET.get('page', 1)

    #print(p.num_pages) #printing total number of pages

    page = p.page(page_num)

    page_obj = p.get_page(page_num)

    #print(page_obj.number) #printing the current page

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.adder = request.user
            instance.save()
            product_name = form.cleaned_data.get('model_name')
            messages.success(request, f'{product_name} has been added.')
            return redirect('dashboard-product1')
    else:
        form = ProductForm()
    context = {
        'page_object': page_obj,
        'p': p,
        'items': page,
        'form': form,
        'workers_count': workers_count,
        'orders_count': orders_count,
        'products_count': products_count,
        'myFilter': myFilter,
    }
    return render(request, 'dashboard/product1.html', context)

@login_required(login_url='user-login')
def product2(request):
    items = Product.objects.all() #Using ORM
    #items = Product.objects.all().order_by('-date') #Using ORM
    products_count = items.count()
    #items = Product.objects.raw('SELECT * FROM dashboard_product')
    workers_count = User.objects.all().count
    orders_count = Order.objects.all().count

    myFilter = ProductFilter(request.GET, queryset=items)

    items = myFilter.qs

    p = Paginator(items, 10)

    page_num = request.GET.get('page', 1)

    #print(p.num_pages) #printing total number of pages

    page = p.page(page_num)

    page_obj = p.get_page(page_num)

    #print(page_obj.number) #printing the current page

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.adder = request.user
            instance.save()
            product_name = form.cleaned_data.get('model_name')
            messages.success(request, f'{product_name} has been added.')
            return redirect('dashboard-product2')
    else:
        form = ProductForm()
    context = {
        'page_object': page_obj,
        'p': p,
        'items': page,
        'form': form,
        'workers_count': workers_count,
        'orders_count': orders_count,
        'products_count': products_count,
        'myFilter': myFilter,
    }
    return render(request, 'dashboard/product2.html', context)

@login_required(login_url='user-login')
def product_delete(request, pk):
    item = Product.objects.get(id=pk)
    system_unit = Component.objects.filter(compo_atn__contains=item.atn)
    if request.method == 'POST':
        item.delete()
        system_unit.delete()
        return redirect('dashboard-product')
    return render(request, 'dashboard/product_delete.html')

@login_required(login_url='user-login')
def product_update(request, pk):
    item = Product.objects.get(id=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('dashboard-product')
    else:
        form = ProductForm(instance=item)
    context ={
        'form':form,
    }
    return render (request, 'dashboard/product_update.html', context)


@login_required(login_url='user-login')
def order(request):
    orders = Order.objects.all()
    orders_count = orders.count()
    workers_count = User.objects.all().count
    products_count = Product.objects.all().count()

    p = Paginator(orders, 50)

    page_num = request.GET.get('page', 1)

    page = p.page(page_num)

    page_obj = p.get_page(page_num)

    item_range = ((p.num_pages - 1) * 50) + 1
    item_range2 = p.num_pages*50

    context={
        'orders': orders,
        'workers_count': workers_count,
        'orders_count': orders_count,
        'products_count': products_count,
        'p': p,
        'page_obj': page_obj,
        'item_range': item_range,
        'item_range2': item_range2,
        'items': page,
    }
    
    return render(request, 'dashboard/order.html', context)

@login_required(login_url='user-login')
def order_staff(request):
    orders = Order.objects.all()
    orders_count = orders.count()
    workers_count = User.objects.all().count
    products_count = Product.objects.all().count()
    context={
        'orders': orders,
        'workers_count': workers_count,
        'orders_count': orders_count,
        'products_count': products_count,
    }
    
    return render(request, 'dashboard/order_staff.html', context)

@login_required(login_url='user-login')
def order_view(request, pk):
    items = Order.objects.get(id=pk)#Using ORM
    #items = Product.objects.all().order_by('-date') #Using ORM
    #products_count = items.count()
    #items = Product.objects.raw('SELECT * FROM dashboard_product')
    #workers_count = User.objects.all().count
    #orders_count = Order.objects.all().count


    #print(p.num_pages) #printing total number of pages

   
    #print(page_obj.number) #printing the current page

    context = {
        'items': items,
    };
    return render(request, 'dashboard/order_view.html', context)

@login_required(login_url='user-login')
def order_approve(request, pk):
    item = Order.objects.get(id=pk)
    if request.method == 'POST':
        Disposal.objects.create(
            disposal_name = item.product.model_name,
            disposal_serial_number = item.product.serial_number,
            remarks = item.disposal_remarks,
        )
        item.delete()
        messages.success(request, f'A job order has been approved!')
        return redirect('dashboard-order')
    return render(request, 'dashboard/job_order_approve.html')


def export_products_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Flipventory_Products.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Products Data') # this will make a sheet named products Data

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['model_name', 'asset_type', 'supplier_name', 'department', 'OR_number', 'serial_number', 'status', 'date']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style) # at 0 row 0 column 

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Product.objects.all().values_list('model_name', 'asset_type', 'supplier_name', 'department', 'OR_number', 'serial_number', 'status', 'date')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)

    return response



@login_required(login_url='user-login')
def product_filter(request):
    items = Product.objects.all() #Using ORM
    products_count = items.count()
    #items = Product.objects.raw('SELECT * FROM dashboard_product')
    workers_count = User.objects.all().count
    orders_count = Order.objects.all().count


    myFilter = ProductFilter(request.GET, queryset=items)

    items = myFilter.qs

    p = Paginator(items, 10)

    page_num = request.GET.get('page', 1)

    #print(p.num_pages) #printing total number of pages

    page = p.page(page_num)

    page_obj = p.get_page(page_num)

    #print(page_obj.number) #printing the current page

    if request.method == 'POST':
        form = ProductFilter(request.POST)
        if form.is_valid():
            messages.success(request, 'Done filtering')
            return redirect('dashboard-product-filter')
    else:
        form = ProductFilter()
    context = {
        'page_object': page_obj,
        'p': p,
        'items': page,
        'form': form,
        'workers_count': workers_count,
        'orders_count': orders_count,
        'products_count': products_count,
        'myFilter': myFilter,
    };
    return render(request, 'dashboard/product_filter.html', context)


@login_required(login_url='user-login')
def product_filter1(request):
    items = Product.objects.all() #Using ORM
    products_count = items.count()
    #items = Product.objects.raw('SELECT * FROM dashboard_product')
    workers_count = User.objects.all().count
    orders_count = Order.objects.all().count

    myFilter = ProductFilter(request.GET, queryset=items)

    items = myFilter.qs

    p = Paginator(items, 10)

    page_num = request.GET.get('page', 1)

    #print(p.num_pages) #printing total number of pages

    page = p.page(page_num)

    page_obj = p.get_page(page_num)

    #print(page_obj.number) #printing the current page

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            product_name = form.cleaned_data.get('model_name')
            messages.success(request, f'{product_name} has been added.')
            return redirect('dashboard-product')
    else:
        form = ProductForm()
    context = {
        'page_object': page_obj,
        'p': p,
        'items': page,
        'form': form,
        'workers_count': workers_count,
        'orders_count': orders_count,
        'products_count': products_count,
        'myFilter': myFilter,
    };
    return render(request, 'dashboard/product_filter1.html', context)

@login_required(login_url='user-login')
def product_filter2(request):
    items = Product.objects.all() #Using ORM
    products_count = items.count()
    #items = Product.objects.raw('SELECT * FROM dashboard_product')
    workers_count = User.objects.all().count
    orders_count = Order.objects.all().count

    myFilter = ProductFilter(request.GET, queryset=items)

    items = myFilter.qs

    p = Paginator(items, 10)

    page_num = request.GET.get('page', 1)

    #print(p.num_pages) #printing total number of pages

    page = p.page(page_num)

    page_obj = p.get_page(page_num)

    #print(page_obj.number) #printing the current page

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            product_name = form.cleaned_data.get('model_name')
            messages.success(request, f'{product_name} has been added.')
            return redirect('dashboard-product')
    else:
        form = ProductForm()
    context = {
        'page_object': page_obj,
        'p': p,
        'items': page,
        'form': form,
        'workers_count': workers_count,
        'orders_count': orders_count,
        'products_count': products_count,
        'myFilter': myFilter,
    };
    return render(request, 'dashboard/product_filter2.html', context)


@login_required(login_url='user-login')
def export_products_csv(request):
    response = HttpResponse(content_type='text/csv')

    writer = csv.writer(response)
    writer.writerow('model_name', 'asset_type', 'supplier_name', 'department', 'OR_number', 'serial_number', 'status', 'date')

    for product in Product.objects.all().values_list('model_name', 'asset_type', 'supplier_name', 'department', 'OR_number', 'serial_number', 'status', 'date'):
        writer.writerow(product)

    response['Content-Disposition'] = 'attachment; filename="Flipventory_Products.csv"'

    return response

@login_required(login_url='user-login')
def productview(request, pk):
    items = Product.objects.get(id=pk)#Using ORM
    #items = Product.objects.all().order_by('-date') #Using ORM
    #products_count = items.count()
    #items = Product.objects.raw('SELECT * FROM dashboard_product')
    #workers_count = User.objects.all().count
    #orders_count = Order.objects.all().count

    print(items.asset_image)
    

    #print(p.num_pages) #printing total number of pages

   
    #print(page_obj.number) #printing the current page

    context = {
        'items': items,
    };
    return render(request, 'dashboard/product_view.html', context)


def about(request):
    #items = Product.objects.get(id=pk)#Using ORM
    #items = Product.objects.all().order_by('-date') #Using ORM
    #products_count = items.count()
    #items = Product.objects.raw('SELECT * FROM dashboard_product')
    #workers_count = User.objects.all().count
    #orders_count = Order.objects.all().count


    

    #print(p.num_pages) #printing total number of pages

   
    #print(page_obj.number) #printing the current page

    context = {
        
    };
    return render(request, 'dashboard/about.html', context)

@login_required(login_url='user-login')
def disposal(request):
    orders = Order.objects.all()
    products = Product.objects.all()
    orders_count = orders.count()
    products_count = products.count()
    workers_count = User.objects.all().count()

    if request.method=='POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.employee = request.user
            instance.save()
            return redirect('dashboard-disposal')
    else:
        form = OrderForm()

    context = {
        'form': form,
        'orders': orders,
        'products': products,
        'orders_count': orders_count,
        'products_count': products_count,
        'workers_count': workers_count,
    };
    return render(request, 'dashboard/employee_index.html', context)

@login_required(login_url='user-login')
def employee_list(request):
    orders = Order.objects.all()
    products = Product.objects.all()
    orders_count = orders.count()
    products_count = products.count()
    workers_count = User.objects.all().count()
    employees = Employee.objects.all()

    empFilter = EmployeeFilter(request.GET, queryset=employees)

    employees = empFilter.qs

    p = Paginator(employees, 50)

    page_num = request.GET.get('page', 1)

    page = p.page(page_num)

    page_obj = p.get_page(page_num)

    item_range = ((p.num_pages - 1) * 50) + 1
    item_range2 = p.num_pages*50


    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            employee_name = form.cleaned_data.get('in_name')
            messages.success(request, f'{employee_name} has been added. Give them a warm welcome.')
            return redirect('dashboard-employee-list')
    else:
        form = EmployeeForm()

    context = {
        'page_object': page_obj,
        'p': p,
        'page': page,
        'employees': employees,
        'form': form,
        'orders': orders,
        'products': products,
        'orders_count': orders_count,
        'products_count': products_count,
        'workers_count': workers_count,
        'item_range': item_range,
        'item_range2': item_range2,
    };
    return render(request, 'dashboard/employee_list.html', context)


@login_required(login_url='user-login')
def employee_delete(request, pk):
    employee = Employee.objects.get(id=pk)
    if request.method == 'POST':
        employee.delete()
        return redirect('dashboard-employee-list')
    return render(request, 'dashboard/employee_delete.html')


@login_required(login_url='user-login')
def procurement(request):
    orders = Order.objects.all()
    items = Product.objects.all()
    items_1 = Product.objects.filter(po__icontains="PO")
    orders_count = orders.count()
    products_count = items.count()
    workers_count = User.objects.all().count()
    employees = Employee.objects.all()

    myFilter_procurement = ProductFilter(request.GET, queryset=items_1)

    items_1 = myFilter_procurement.qs

    p = Paginator(items_1, 50)

    page_num = request.GET.get('page', 1)

    page = p.page(page_num)

    page_obj = p.get_page(page_num)

    item_range = ((p.num_pages - 1) * 50) + 1
    item_range2 = p.num_pages*50

    if request.method == 'POST':
        form = ProcurementForm(request.POST)
        form1 = ComponentForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.adder = request.user
            if instance.asset_type == "Hard Disk Drive":
                instance.classification = "001"
            elif instance.asset_type == "Solid State Drive":
                instance.classification = "002"
            elif instance.asset_type == "Graphics Card":
                instance.classification = "003"
            elif instance.asset_type == "Laptop":
                instance.classification = "004"
            elif instance.asset_type == "RAM":
                instance.classification = "005"    
            elif instance.asset_type == "Charger":
                instance.classification = "006"
            elif instance.asset_type == "UPS":
                instance.classification = "007"
            elif instance.asset_type == "Mouse":
                instance.classification = "008"
            elif instance.asset_type == "Keyboard":
                instance.classification = "009"
            elif instance.asset_type == "Motherboard":
                instance.classification = "010"
            elif instance.asset_type == "Monitor":
                instance.classification = "011"
            elif instance.asset_type == "Power Supply":
                instance.classification = "012"
            elif instance.asset_type == "Router":
                instance.classification = "013"
            elif instance.asset_type == "AVR":
                instance.classification = "014"
            elif instance.asset_type == "Tablet":
                instance.classification = "015"
            elif instance.asset_type == "System Unit":
                instance.classification = "016"
            elif instance.asset_type == "Audio Devices":
                instance.classification = "017"
            elif instance.asset_type == "CPU":
                instance.classification = "018"
            else:
                instance.classification = "019"
            
            #product_name = form.cleaned_data.get('model_name')
            messages.success(request, 'Procured item has been added.')
            instance.save()
            return redirect('dashboard-procurement')
    else:
        form = ProcurementForm()

    context = {
        'employees': employees,
        'form': form,
        'orders': orders,
        'items': items,
        'items_1': items_1,
        'orders_count': orders_count,
        'products_count': products_count,
        'workers_count': workers_count,
        'item_range': item_range,
        'item_range2': item_range2,
        'page_object': page_obj,
        'p': p,
        'items1': page,
    };
    return render(request, 'dashboard/procurement.html', context)


@login_required(login_url='user-login')
def component(request):
    orders = Order.objects.all()
    items = Product.objects.all()
    orders_count = orders.count()
    products_count = items.count()
    workers_count = User.objects.all().count()
    employees = Employee.objects.all()
    assembled = Component.objects.all()

    myFilter_component = ComponentFilter(request.GET, queryset=assembled)

    assembled = myFilter_component.qs

    p = Paginator(assembled, 50)

    page_num = request.GET.get('page', 1)

    page = p.page(page_num)

    page_obj = p.get_page(page_num)

    item_range = ((p.num_pages - 1) * 50) + 1
    item_range2 = p.num_pages*50

    if request == 'POST':
        form = ComponentForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Changes has been saved.')
            form.save()
            return redirect('dashboard-component')
    else:
        form = ComponentForm()


    context = {
        'employees': employees,
        'orders': orders,
        'items': items,
        'orders_count': orders_count,
        'products_count': products_count,
        'workers_count': workers_count,
        'assembled': assembled,
        'form': form,
        'item_range': item_range,
        'item_range2': item_range2,
        'page_object': page_obj,
        'p': p,
        'component': page,
    };

    return render(request, 'dashboard/assembly.html', context)


@login_required(login_url='user-login')
def component_view(request, pk):
    orders = Order.objects.all()
    items = Product.objects.all()
    orders_count = orders.count()
    products_count = items.count()
    workers_count = User.objects.all().count()
    employees = Employee.objects.all()
    assembled = Component.objects.get(id=pk)

    if request == 'POST':
        form = ComponentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard-component')
    else:
        form = ComponentForm()


    context = {
        'employees': employees,
        'orders': orders,
        'items': items,
        'orders_count': orders_count,
        'products_count': products_count,
        'workers_count': workers_count,
        'assembled': assembled,
        'form': form,
    };

    return render(request, 'dashboard/assembly_view.html', context)

@login_required(login_url='user-login')
def assembly_update(request, pk):
    component = Component.objects.get(id=pk)
    if request.method == 'POST':
        form = ComponentForm(request.POST, request.FILES, instance=component)
        if form.is_valid():
            form.save()
            return redirect('dashboard-component')
    else:
        form = ComponentForm(instance=component)
    context ={
        'form':form,

    }
    return render (request, 'dashboard/assembly_update.html', context)


@login_required(login_url='user-login')
def allocation_view(request):
    orders = Order.objects.all()
    items = Product.objects.all()
    orders_count = orders.count()
    products_count = items.count()
    workers_count = User.objects.all().count()
    employees = Employee.objects.all()
    allocated = Allocation.objects.all()

    myFilter_allocation = AllocationFilter(request.GET, queryset=allocated)

    allocated = myFilter_allocation.qs

    p = Paginator(allocated, 50) #nagsasabi kung ilang item per page
    page_num = request.GET.get('page', 1) #page getter initialize
    page = p.page(page_num)
    page_obj = p.get_page(page_num)

    item_range = ((p.num_pages - 1) * 50) + 1
    item_range2 = p.num_pages*50

    if request.method == 'POST':
        form = AllocationForm(request.POST, request.FILES)
        if form.is_valid():
            messages.success(request, 'Allocation has been added.')
            form.save()
            return redirect('dashboard-allocation')  
        else:
            messages.warning(request, 'A device has been allocated already, please check again.')
    else:
        form = AllocationForm()
        

    context = {
        'employees': employees,
        'orders': orders,
        'items': items,
        'orders_count': orders_count,
        'products_count': products_count,
        'workers_count': workers_count,
        'form': form,
        'allocated': allocated,
        'page_object': page_obj,
        'p': p,
        'allocated1': page,
        'item_range': item_range,
        'item_range2': item_range2,
        'allocated': allocated,
        };

    return render(request, 'dashboard/allocation.html', context)


@login_required(login_url='user-login')
def malfunction_view(request):
    items = Product.objects.filter(status="Not Working")
    products_count = items.count()
    workers_count = User.objects.all().count()
     

    context = {
        'items': items,
        'products_count': products_count,
        'workers_count': workers_count,
    };

    return render(request, 'dashboard/malfunction.html', context)

@login_required(login_url='user-login')
def no_image_view(request):
    items = Product.objects.filter(asset_image="Product_Default.png")
    products_count = items.count()
    workers_count = User.objects.all().count()
     

    context = {
        'items': items,
        'products_count': products_count,
        'workers_count': workers_count,
    };

    return render(request, 'dashboard/no_image.html', context)

@login_required(login_url='user-login')
def overall_filter(request):
    orders = Order.objects.all()
    items = Product.objects.all()
    orders_count = orders.count()
    products_count = items.count()
    workers_count = User.objects.all().count()
    employees = Employee.objects.all()
    allocated = Allocation.objects.all()


    context ={
        'employees': employees,
        'orders': orders,
        'items': items,
        'orders_count': orders_count,
        'products_count': products_count,
        'workers_count': workers_count,
        'allocated': allocated,
    }
    return render (request, 'dashboard/overall_filter.html', context)


@login_required(login_url='user-login')
def emp_filter(request):
    orders = Order.objects.all()
    items = Product.objects.all()
    orders_count = orders.count()
    products_count = items.count()
    workers_count = User.objects.all().count()
    employees = Employee.objects.all()
    allocated = Allocation.objects.all()

    myFilter = EmployeeFilter(request.GET, queryset=employees)

    employees = myFilter.qs

    p = Paginator(employees, 9)

    page_num = request.GET.get('page', 1)

    #print(p.num_pages) #printing total number of pages

    page = p.page(page_num)

    page_obj = p.get_page(page_num)

    #print(page_obj.number) #printing the current page

    if request.method == 'POST':
        form = EmployeeFilter(request.POST)
        if form.is_valid():
            messages.success(request, 'Done filtering')
            return redirect('dashboard-product-filter')
    else:
        form = EmployeeFilter()

    context ={
        'employees': employees,
        'orders': orders,
        'items': items,
        'orders_count': orders_count,
        'products_count': products_count,
        'workers_count': workers_count,
        'allocated': allocated,
        'myFilter': myFilter,
        'page': page,
        'p': p,
        'page_object': page_obj
    }
    return render (request, 'dashboard/employee_filter.html', context)


@login_required(login_url='user-login')
def alloc_filter(request):
    orders = Order.objects.all()
    items = Product.objects.all()
    orders_count = orders.count()
    products_count = items.count()
    workers_count = User.objects.all().count()
    employees = Employee.objects.all()
    allocated = Allocation.objects.all()

    myFilter = AllocationFilter(request.GET, queryset=allocated)

    allocated = myFilter.qs

    p = Paginator(allocated, 8)

    page_num = request.GET.get('page', 1)

    #print(p.num_pages) #printing total number of pages

    page = p.page(page_num)

    page_obj = p.get_page(page_num)

    #print(page_obj.number) #printing the current page

    if request.method == 'POST':
        form = AllocationFilter(request.POST)
        if form.is_valid():
            messages.success(request, 'Done filtering')
            return redirect('dashboard-product-filter')
    else:
        form = AllocationFilter()

    context ={
        'employees': employees,
        'orders': orders,
        'items': items,
        'orders_count': orders_count,
        'products_count': products_count,
        'workers_count': workers_count,
        'allocated': allocated,
        'myFilter': myFilter,
        'page': page,
        'p': p,
        'page_object': page_obj
    }
    return render (request, 'dashboard/allocation_filter.html', context)

@login_required(login_url='user-login')
def compo_filter(request):
    orders = Order.objects.all()
    items = Product.objects.all()
    orders_count = orders.count()
    products_count = items.count()
    workers_count = User.objects.all().count()
    employees = Employee.objects.all()
    allocated = Allocation.objects.all()
    component_all = Component.objects.all()

    myFilter = ComponentFilter(request.GET, queryset=component_all)

    component_all = myFilter.qs

    p = Paginator(component_all, 8)

    page_num = request.GET.get('page', 1)

    #print(p.num_pages) #printing total number of pages

    page = p.page(page_num)

    page_obj = p.get_page(page_num)

    #print(page_obj.number) #printing the current page

    if request.method == 'POST':
        form = ComponentFilter(request.POST)
        if form.is_valid():
            messages.success(request, 'Done filtering')
            return redirect('dashboard-product-filter')
    else:
        form = ComponentFilter()

    context ={
        'employees': employees,
        'orders': orders,
        'items': items,
        'orders_count': orders_count,
        'products_count': products_count,
        'workers_count': workers_count,
        'allocated': allocated,
        'myFilter': myFilter,
        'component': page,
        'p': p,
        'page_object': page_obj
    }
    return render (request, 'dashboard/component_filter.html', context)


@login_required(login_url='user-login')
def final_disposal(request):
    disposals = Disposal.objects.all()
    orders_count = Order.objects.all()
    workers_count = User.objects.all().count
    products_count = Product.objects.all().count()

    p = Paginator(disposals, 50)

    page_num = request.GET.get('page', 1)

    page = p.page(page_num)

    page_obj = p.get_page(page_num)

    item_range = ((p.num_pages - 1) * 50) + 1
    item_range2 = p.num_pages*50

    context={
        'disposals': disposals,
        'workers_count': workers_count,
        'orders_count': orders_count,
        'products_count': products_count,
        'p': p,
        'page_obj': page_obj,
        'items': page,
        'item_range': item_range,
        'item_range2': item_range2,
    }
    return render(request, 'dashboard/disposal.html', context)


@login_required(login_url='user-login')
def error_404(request,exception):
    context={
    }
    return render(request, 'dashboard/404.html', context)


def simple_upload(request):
    if request.method == 'POST':
        person_resource = EmployeeResource()
        dataset = Dataset()
        new_person = request.FILES['myfile']

        if not new_person.name.endswith('xlsx'):
            message.info(request, 'wrong format')
            return render(request, 'upload.html')