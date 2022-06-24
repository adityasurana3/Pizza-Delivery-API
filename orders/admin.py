from ast import Or
from django.contrib import admin
from  .models import Order

# Register your models here.

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['size','order_status']
    list_filter= ['size','order_status','created_at','updated_at']