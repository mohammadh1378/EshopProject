from django.db.models import Q
from django.db import models
import os
from eshop_products_category.models import ProductCategory


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f"{instance.id}-{instance.title}{ext}"
    return f"products/{final_name}"


def upload_gallery_image_path(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f"{instance.id}-{instance.title}{ext}"
    return f"products/galleries/{final_name}"


# Create your models here.

class ProductsManager(models.Manager):
    def get_active_products(self):
        return self.get_queryset().filter(active=True)

    def get_products_by_category(self, category_name):
        return self.get_queryset().filter(categories__name__iexact=category_name, active=True)

    def get_by_id(self, product_id):
        qs = self.get_queryset().filter(id=product_id)
        if qs.count() == 1:
            return qs.first()
        else:
            return None

    def search(self, query):
        lookup = (
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(tag__title__icontains=query)
        )
        return self.get_queryset().filter(lookup, active=True).distinct()


class Product(models.Model):
    title = models.CharField(max_length=150, verbose_name='عنوان')
    description = models.TextField(verbose_name='توضیحات')
    price = models.IntegerField(verbose_name='قیمت')
    image = models.ImageField(upload_to=upload_image_path, null=True, blank=True, verbose_name='تصویر')
    active = models.BooleanField(default=False, verbose_name='فعال / غیرفعال')
    categories = models.ManyToManyField(ProductCategory, blank=True, verbose_name="دسته بندی ها")
    available = models.BooleanField(default=True, verbose_name='موجود در انبار')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ساخت محصول')
    updated = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    count = models.IntegerField(default=0, verbose_name='تعداد موجود در انبار')
    count_sold = models.IntegerField(default=0, verbose_name='تعداد فروخته شده')

    objects = ProductsManager()

    class Meta:
        ordering = ('title',)
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"/products/{self.id}/{self.title.replace(' ', '-')}"

    def new_quantity_product(self, order_quantity):
        new_quantity = self.count - order_quantity
        self.count_sold += order_quantity
        self.count = new_quantity
        Product.objects.filter(id=self.id).update(count=self.count, count_sold=self.count_sold)


class ProductGallery(models.Model):
    title = models.CharField(max_length=150, verbose_name='عنوان')
    image = models.ImageField(upload_to=upload_gallery_image_path, verbose_name='تصویر')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')

    class Meta:
        verbose_name = 'تصویر'
        verbose_name_plural = 'تصاویر'

    def __str__(self):
        return self.title


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments', verbose_name='محصول')
    name = models.CharField(max_length=80, verbose_name='نام')
    email = models.EmailField(verbose_name='ایمیل')
    body = models.TextField(verbose_name='متن')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')
    updated = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    active = models.BooleanField(default=True, verbose_name='فعال')

    class Meta:
        ordering = ('created',)
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'

    def __str__(self):
        return f'نظر توسط {self.name} در محصول {self.product}'
