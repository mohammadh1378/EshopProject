from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, verbose_name='نام', blank=True, null=True)
    last_name = models.CharField(max_length=50, verbose_name='نام خانوادگی', blank=True, null=True)
    phone_number = models.CharField(max_length=11, verbose_name='شماره تلفن', blank=True, null=True)
    address = models.CharField(max_length=250, verbose_name='آدرس', blank=True, null=True)
    postal_code = models.CharField(max_length=20, verbose_name='کد پستی', blank=True, null=True)
    city = models.CharField(max_length=100, verbose_name='شهر', blank=True, null=True)

    class Meta:
        verbose_name = 'پروفایل کاربر'
        verbose_name_plural = 'پروفایل کاربران'

    def __str__(self):
        return f'پروفایل برای کاربر {self.user.username}'

