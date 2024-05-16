from django.shortcuts import render

from django.views.generic.base import TemplateView
from dashboard.filters import ProductFilter

class ExcelPageView(TemplateView):
    template_name = "excel_app.html"

# Create your views here.
# excel_app/views.py

import xlwt
from django.http import HttpResponse
from django.contrib.auth.models import User
from dashboard.models import Product

def export_products_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="products.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Products Data') # this will make a sheet named products Data

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['name', 'category', 'subcategory', 'quantity', 'department', 'status']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style) # at 0 row 0 column 

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Product.objects.all().values_list('name', 'category', 'subcategory', 'quantity', 'department', 'status')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)

    return response