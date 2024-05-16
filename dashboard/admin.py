from django.contrib import admin
from .models import Product, Order, Employee, Component, Allocation, Disposal
from django.contrib.auth.models import Group
from django.contrib.admin.models import LogEntry, DELETION
from django.contrib import admin
from django.utils.html import escape
from django.urls import reverse
from django.utils.safestring import mark_safe
from import_export.admin import ImportExportModelAdmin


# Register your models here.

admin.site.site_header = 'Flipventory Admin Panel'
admin.site.site_title = 'Flipventory Admin Panel'

class AllocationAdmin(admin.ModelAdmin):
    list_display = ('allocation_employee', 'location', 'asset_allocation', 'system_allocation', 'alloc_date')
    list_filter = ('location',)
    search_fields = ('location',)

class ComponentAdmin(admin.ModelAdmin):
    list_display = ('catn', 'compo_atn', 'compo_name')
    search_fields = ('compo_atn',)

class ProductsAdmin(admin.ModelAdmin):
    readonly_fields = ('id','atn', 'po')
    list_display = ('model_name', 'asset_type', 'supplier_name', 'department', 'OR_number', 'serial_number', 'status', 'date')
    list_filter = ('asset_type', 'department', 'status')
    search_fields = ('model_name',)

class OrdersAdmin(admin.ModelAdmin):
    list_display = ('product', 'employee',)
    list_filter = ('date',)

class EmployeeAdmin(ImportExportModelAdmin):
    list_display = ('in_name', 'out_name',)
    list_filter = ('emp_department',)
    search_fields = ('in_name',)

class LogEntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'action_time'

    list_filter = [
        'user',
        'content_type',
        'action_flag'
    ]

    search_fields = [
        'object_repr',
        'change_message'
    ]

    list_display = [
        'action_time',
        'user',
        'content_type',
        'object_link',
        'action_flag',
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def object_link(self, obj):
        if obj.action_flag == DELETION:
            link = escape(obj.object_repr)
        else:
            ct = obj.content_type
            link = '<a href="%s">%s</a>' % (
                reverse('admin:%s_%s_change' % (ct.app_label, ct.model), args=[obj.object_id]),
                escape(obj.object_repr),
            )
        return mark_safe(link)
    object_link.admin_order_field = "object_repr"
    object_link.short_description = "object"


admin.site.register(Allocation, AllocationAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Disposal)
admin.site.register(Product, ProductsAdmin)
admin.site.register(Order, OrdersAdmin)
admin.site.register(Component, ComponentAdmin)
admin.site.register(LogEntry, LogEntryAdmin)
#admin.site.unregister(Group)



