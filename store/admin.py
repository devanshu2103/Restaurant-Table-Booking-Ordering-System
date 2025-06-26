from django.contrib import admin
from .models import TableCategory, Booking, MenuItem, Order

@admin.register(TableCategory)
class TableCategoryAdmin(admin.ModelAdmin):
    list_display = ('category', 'available_tables') 

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'table_type', 'booking_time', 'duration', 'release_time')

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')  

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('booking', 'item', 'quantity')  

 