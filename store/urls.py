from django.contrib.auth import logout, login
from django.urls import path

from store.Views.CartView import cart_view
from store.Views.brandView import BrandView
from store.Views.insert_data import insert_data
from store.Views.mainPageView import ViewMain
from store.Views.categoriesView import CategoryView
from store.Views.productView import ProductView
from store.Views.productsView import ProductsView
from store.Views.UserView import ProfileView, sign_in, sign_up, sign_out
from store.Views.favoriteView import favorite_view

urlpatterns = [
    path('store/insert/', insert_data, name="insert"),
    path('store/<slug:catalog>/', ViewMain.as_view(), name="view_main"),
    path("store/<slug:catalog>/category/<slug:category>", CategoryView.as_view(), name="category_view"),
    path("store/<slug:catalog>/products/<slug:category>/", ProductsView.as_view(), name="products_view"),
    path("store/<slug:catalog>/products/<slug:category>", ProductsView.as_view(), name="products_view"),
    path("store/<slug:catalog>/brand/<slug:brand>", BrandView.as_view(), name="brand_view"),
    path("store/<slug:catalog>/<slug:category>/<slug:product>", ProductView.as_view(), name="product"),
    path("store/<slug:catalog>/<slug:category>/<slug:product>/characteristics", ProductView.as_view(), name="product"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path('login/', sign_in, name='login'),
    path('logout/', sign_out, name='logout'),
    path('register/', sign_up, name='register'),
    path("cart/", cart_view, name='cart'),
    path('favorites/', favorite_view, name='favorite')
]
