from django.db.models import Q
from django.views.generic import ListView
from store.Views.productsView import GetProductMixin
from store.models import Brands, Categories


class ViewMain(GetProductMixin, ListView):
    model = Categories
    template_name = "mainPageTemplate.html"
    context_object_name = "categories"
    http_method_names = ['get']
    slug_url_kwarg = 'catalog'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brands'] = Brands.objects.filter(~Q(logo="brand_image\\"))[0:5]
        context['products'] = super().get_products()
        return context

    def get_queryset(self):
        return self.model.objects.filter(parent_id=self.model.objects.get(parent_id=None))

