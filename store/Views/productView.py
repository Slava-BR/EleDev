import json

from django.views.generic import DetailView
from store.models import Products, Images,  Descriptions


class ProductView(DetailView):
    model = Products
    context_object_name = "product"
    slug_url_kwarg = "product"
    template_name = "productTemplate.html"
    http_method_names = ['get', 'post']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'characteristic' in self.request.build_absolute_uri():
            description = Descriptions.objects.get(product_id=context["product"].product_code)
            context['characteristics'] = json.loads(description.characteristic)
            context['description'] = description.description
        else:
            context['characteristics'] = None
        context["image"] = Images.objects.filter(product_id=context["product"].product_code)[0]
        return context
