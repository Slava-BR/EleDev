from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from store.models import User, FavoritesProducts


@login_required(login_url='/login/')
def favorite_view(request):
    products = FavoritesProducts.objects.get(user=User.objects.get(username=request.user.username)).products.all()
    return render(request, "favorite.html", {'products': products})
