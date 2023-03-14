from django.contrib import admin
from .models import Item, OrderItem ,Order,Address

class OrderAdmin(admin.ModelAdmin):
    list_display=['user','ordered','get_order_cost']

class AddressAdmin(admin.ModelAdmin):
    list_display=[
    'user',
    'first_name',
    'last_name',
    'street_address',
    'apartment_address',
    'country',
    'city',
    'postal_code',
    'phone',
]


admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order,OrderAdmin)
admin.site.register(Address,AddressAdmin)
