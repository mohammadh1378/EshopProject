from django.contrib import admin

# Register your models here.

from .models import Product, ProductGallery, Comment


class ProductAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'title', 'price', 'active',
                    'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']

    class Meta:
        model = Product


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'product', 'created', 'active']
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductGallery)
