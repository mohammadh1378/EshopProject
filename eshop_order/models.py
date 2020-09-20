from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from eshop_account.models import Profile
from eshop_products.models import Product


class NewOrder(models.Model):
    first_name = models.CharField(max_length=50, verbose_name='نام',)
    last_name = models.CharField(max_length=50, verbose_name='نام خانوادگی')
    email = models.EmailField(verbose_name='ایمیل')
    phone_number = models.CharField(max_length=11, verbose_name='شماره تلفن')
    address = models.CharField(max_length=250, verbose_name='آدرس')
    postal_code = models.CharField(max_length=20, verbose_name='کد پستی')
    city = models.CharField(max_length=100, verbose_name='شهر')
    created = models.DateTimeField(auto_now_add=True, verbose_name='ساخته شده')
    updated = models.DateTimeField(auto_now=True, verbose_name='بروز شده')
    paid = models.BooleanField(default=False, verbose_name='پرداخت شده')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'سفارش کاربر'
        verbose_name_plural = 'سفارش های کاربران'

    def __str__(self):
        return f'سفارش {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(NewOrder,
                              related_name='items',
                              on_delete=models.CASCADE, verbose_name='سفارش')
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE, verbose_name='محصول')

    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='قیمت')
    quantity = models.PositiveIntegerField(default=1, verbose_name='تعداد')

    class Meta:
        verbose_name = 'محصول سفارش داده شده'
        verbose_name_plural = 'محصولات سفارش داده شده'

    def __str__(self):
        return f'سفارش کاربر {self.order.first_name}'

    def get_cost(self):
        return self.price * self.quantity

