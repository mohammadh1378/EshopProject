from django.contrib import admin

# Register your models here.
# from eshop_order.models import Order, OrderDetail
#
# admin.site.register(Order)
# admin.site.register(OrderDetail)

from django.contrib import admin

from .models import NewOrder, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(NewOrder)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'phone_number',
                    'address', 'postal_code', 'city', 'paid',
                    'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]



