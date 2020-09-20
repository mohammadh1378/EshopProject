from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

# Create your views here.
from cart.cart import Cart
from eshop_order.forms import UserNewOrderForm, OrderCreateForm
from eshop_order.models import OrderItem
from eshop_products.models import Product
from .tasks import order_created


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = OrderCreateForm(request.POST, initial={'first_name': request.user.profile.first_name,
                                                          'last_name': request.user.profile.last_name,
                                                          'email': request.user.email,
                                                          'phone_number': request.user.profile.phone_number,
                                                          'city': request.user.profile.city,
                                                          'postal_code': request.user.profile.postal_code,
                                                          'address': request.user.profile.address})
        else:
            form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                if item['quantity'] <= item['product'].count:
                    OrderItem.objects.create(order=order,
                                             product=item['product'],
                                             price=item['price'],
                                             quantity=item['quantity'])
                    Product.new_quantity_product(item['product'], item['quantity'])
                else:
                    context = {
                        'error_message': messages.error(request, "این تعداد در انبار موجود نمیباشد")
                    }
                    return render(request, 'cart/detail.html', context)
            # clear the cart
            cart.clear()
            # launch asynchronous task
            order_created.delay(order.id)
            return render(request,
                          'order/created.html',
                          {'order': order})

    else:
        if request.user.is_authenticated:
            form = OrderCreateForm(initial={'first_name': request.user.profile.first_name,
                                            'last_name': request.user.profile.last_name,
                                            'email': request.user.email,
                                            'phone_number': request.user.profile.phone_number,
                                            'city': request.user.profile.city,
                                            'postal_code': request.user.profile.postal_code,
                                            'address': request.user.profile.address})
        else:
            form = OrderCreateForm()
    return render(request,
                  'order/create.html',
                  {'cart': cart, 'form': form, 'title': 'سفارش'})
