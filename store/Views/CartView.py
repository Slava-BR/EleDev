from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from store.models import Products


@login_required(login_url='/login/')
def cart_view(request):
    products = {}
    try:
        for product in request.session['session']['cart']:
            try:
                products[Products.objects.get(product_code=product)] += 1
            except KeyError:
                products[Products.objects.get(product_code=product)] = 1
    except KeyError:
        pass
    return render(request, "cartView.html", {'products': products})
