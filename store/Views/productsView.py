from django.contrib.auth.models import User
from django.views.generic import ListView

from store.forms import CharacteristicForm

from store.models import Products, Images, Categories, Brands, FavoritesProducts


class GetProductMixin:
    product_class = Products
    image_class = Images
    product_in_line = 4
    count = 0
    slug = ""

    def get_products(self):
        """Depending on the slug, select the desired filter and model"""
        if self.kwargs[self.slug_url_kwarg] == 'Catalog':
            self.kwargs[self.slug_url_kwarg] = 'Sale'
        slug_filter = {'brand': 'brand_id',
                       'category': 'category_product',
                       'catalog': 'category_product',
                       }
        slug_func = {'brand': Brands.objects.get,
                     'category': Categories.objects.get,
                     'catalog': Categories.objects.get}
        # SESSION
        if self.request.user.is_authenticated:
            try:
                code = self.request.GET['fav']
                obj, bl = FavoritesProducts.objects.get_or_create(user=User.objects.get(username=self.request.user.username))
                obj.products.add(Products.objects.get(product_code=code))
            except KeyError:
                pass
            try:
                code = self.request.GET['cart']
                try:
                    self.request.session['session']['cart'].append(code)
                except KeyError:
                    self.request.session['session'] = {'cart': [code]}
                self.request.session.modified = True
            except KeyError:
                pass
        # Compare
        # try:
        #     code = self.request.GET['compare']
        #     try:
        #         self.request.session['session']['compare'][1] = code
        #     except KeyError:
        #         self.request.session['session'] = {'compare': [code, None]}
        #     self.request.session.modified = True
        # except KeyError:
        #     pass
        #FIlTER
        # f = False
        # descriptions = {}
        # for key, value in self.request.GET.items():
        #     if key == "p":
        #         break
        #     if value == "":
        #         continue
        #
        #     for i in range(len(self.request.GET)):
        #         descriptions = Descriptions.objects.filter({"characteristic__" + f"{i}__" + key: value})
        #     f = True
        # if f:
        #     products = [Products.objects.get(i.product_code) for i in descriptions]
        # else:

        self.slug = self.kwargs[self.slug_url_kwarg]
        products = self.product_class.objects.filter(**{slug_filter[self.slug_url_kwarg]:
                                                          slug_func[self.slug_url_kwarg](slug=self.kwargs[self.slug_url_kwarg]).id})
        products_table = []
        product_line = []
        for i, product in enumerate(products):
            if i % self.product_in_line == 0 and i != 0:
                products_table.append(product_line)
                product_line = []
            product_line.append([product, self.image_class.objects.get(product_id=product.product_code)])
        if product_line:
            products_table.append(product_line)
        self.count = products.count()
        return products_table


class ProductsView(GetProductMixin, ListView):
    model = Products
    context_object_name = 'products'
    template_name = "productsTemplate.html"
    http_method_names = ['get', 'post']
    slug_url_kwarg = "category"
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count'] = self.count
        context['slug'] = self.slug
        context['p'] = self.request.GET.get('p')
        context['characteristic'] = Categories.objects.get(slug=context['slug']).default_characteristic
        context['form'] = CharacteristicForm(characteristic=context['characteristic'])
        return context

    def get_queryset(self):
        return super().get_products()

