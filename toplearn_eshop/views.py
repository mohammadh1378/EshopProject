from django.shortcuts import render, render_to_response
from django.template import RequestContext

from eshop_products.models import Product
from eshop_products.views import my_grouper
from eshop_products_category.models import ProductCategory
from eshop_sliders.models import Slider
from eshop_settings.models import SiteSetting


# header code behind
def header(request, *args, **kwargs):
    site_setting = SiteSetting.objects.first()
    context = {
        'setting': site_setting
    }
    return render(request, 'shared/Header.html', context)


# footer code behind
def footer(request, *args, **kwargs):
    site_setting = SiteSetting.objects.first()
    categories = ProductCategory.objects.all()[:5]

    context = {
        'categories': categories,
        'setting': site_setting
    }
    return render(request, 'shared/Footer.html', context)


# code behind
def home_page(request):
    sliders = Slider.objects.all()
    all_latest_products = Product.objects.filter(active=True, available=True).order_by('-created')[:12]
    all_best_sellers = Product.objects.filter(active=True, available=True).order_by('-count_sold')[:12]
    best_sellers = my_grouper(4, all_best_sellers)
    latest_products = my_grouper(4, all_latest_products)
    context = {
        'title': 'صفحه اصلی',
        'latest_products': latest_products,
        'best_sellers': best_sellers,
        'sliders': sliders
    }
    return render(request, 'home_page.html', context)


def about_page(request):
    site_setting = SiteSetting.objects.first()
    context = {
        'title': 'درباره ما',
        'setting': site_setting
    }
    return render(request, 'about_page.html', context)

# def handler404(request, *args, **argv):
#     response = render_to_response('404.html', {})
#     response.status_code = 404
#     return response
