from django.views.generic import DetailView
from store.Views.productsView import GetProductMixin
from store.models import Brands


class BrandView(GetProductMixin, DetailView):
    model = Brands
    template_name = "brand.html"
    context_object_name = "brand"
    http_method_names = ['get']
    slug_url_kwarg = "brand"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = super().get_products()
        return context
