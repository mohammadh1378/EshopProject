import itertools
from cart.forms import CartAddProductForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import ListView

from eshop_order.forms import UserNewOrderForm
from .models import Product, ProductGallery, Comment
from .forms import CommentForm
from django.http import Http404
from eshop_products_category.models import ProductCategory


# Create your views here.

class ProductsList(ListView):
    template_name = 'products/products_list.html'
    paginate_by = 6

    def get_queryset(self):
        return Product.objects.get_active_products()


class ProductsListByCategory(ListView):
    template_name = 'products/products_list.html'
    paginate_by = 6

    def get_queryset(self):
        print(self.kwargs)
        category_name = self.kwargs['category_name']
        category = ProductCategory.objects.filter(name__iexact=category_name).first()
        if category is None:
            raise Http404('صفحه ی مورد نظر یافت نشد')
        return Product.objects.get_products_by_category(category_name)


def my_grouper(n, iterable):
    args = [iter(iterable)] * n
    return ([e for e in t if e is not None] for t in itertools.zip_longest(*args))


def product_detail(request, *args, **kwargs):
    selected_product_id = kwargs['productId']
    new_order_form = UserNewOrderForm(request.POST or None, initial={'product_id': selected_product_id})
    cart_product_form = CartAddProductForm()
    product = Product.objects.get_by_id(selected_product_id)

    if product.count <= 0:
        product.available = False

    if product is None or not product.active:
        raise Http404('محصول مورد نظر یافت نشد')

    related_products = Product.objects.get_queryset().filter(categories__product=product).distinct()

    grouped_related_products = my_grouper(3, related_products)

    galleries = ProductGallery.objects.filter(product_id=selected_product_id)

    grouped_galleries = list(my_grouper(3, galleries))

    # active comments for this product
    comments = product.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        if request.user.is_authenticated:
            comment_form = CommentForm(data=request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.product = product
                new_comment.save()
        else:
            return redirect('/login')
    else:
        comment_form = CommentForm()

    context = {
        'product': product,
        'galleries': grouped_galleries,
        'related_products': grouped_related_products,
        'new_order_form': new_order_form,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
        'cart_product_form': cart_product_form
    }

    return render(request, 'products/product_detail.html', context)


class SearchProductsView(ListView):
    template_name = 'products/products_list.html'
    paginate_by = 6

    def get_queryset(self):
        request = self.request
        print(request.GET)
        query = request.GET.get('q')
        if query is not None:
            return Product.objects.search(query)

        return Product.objects.get_active_products()


def products_categories_partial(request):
    categories = ProductCategory.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'products/products_categories_partial.html', context)
