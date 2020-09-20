from django.contrib import admin

# Register your models here.
from eshop_account.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'phone_number',
                    'address', 'postal_code', 'city']