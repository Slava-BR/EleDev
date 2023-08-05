from django.views.generic import DetailView, ListView
from store.models import Categories, Products, Images


class CategoryView(ListView):
    model = Categories
    template_name = "categoriesTemplate.html"
    context_object_name = "categories"
    http_method_names = ['get']
    slug_url_kwarg = "category"

    def get_queryset(self):
        """get all categories whose ancestor is specified in the url"""
        categories = self.model.objects.filter(parent_id=self.model.objects.get(slug=self.kwargs[self.slug_url_kwarg]))
        return [categories[i * 5:(i + 1) * 5] for i in range(len(categories))]
