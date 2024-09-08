from django.contrib import admin
from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_owner', 'is_employee']


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Restaurant)
admin.site.register(Employee)
admin.site.register(Category)
admin.site.register(Menu)
admin.site.register(FoodItem)
admin.site.register(Modifier)
admin.site.register(Order)
