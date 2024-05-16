from django.contrib import admin
from .models import Profile, User


# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('employee', 'role', 'role_department')
    list_filter = ('role', 'role_department')


admin.site.register(Profile, ProfileAdmin)


