import time

from django.http import HttpResponse
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView

from apps.models import Product, ProductImage, Category
from apps.tasks import send_mail_func


# Create your views here.
class ProductListView(ListView):
    template_name = 'apps/product grid.html'
    context_object_name = 'products'
    paginate_by = 9

    def get_queryset(self):
        category_id = self.request.path.split('/')[-1]
        if category_id:
            return Product.objects.filter(category_id=category_id)
        return Product.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        contex = super().get_context_data(**kwargs)
        contex['categories'] = Category.objects.all()
        return contex


class SendMailView(View):
    def get(self, request, *args, **kwargs):
        subject = 'Welcome to My Site'
        message = 'Thank you for creating an account!'
        recipient_list = request.GET.get('email')
        start = time.time()
        # add(5)  # simple
        send_mail_func.delay()  # celery
        # send_mail(subject, message, EMAIL_HOST_USER, [recipient_list])
        end = time.time()
        return HttpResponse(f'saytga yuborildi{end - start}')


class FilteredCategoriesListView(ListView):
    model = Product
    template_name = 'apps/categories.html'
    context_object_name = 'category'

    def get_queryset(self):
        category_id = self.request.GET.get('category', None)
        if category_id:
            return self.queryset.filter(category_id=category_id)
        return super().get_queryset()


class MarketListView(ListView):
    paginate_by = 9
    model = Product
    queryset = Product.objects.order_by('-id')
    template_name = 'apps/market.html'
    context_object_name = 'market_list'

    def get_queryset(self):
        category_id = self.request.GET.get('category', None)
        if category_id:
            return self.queryset.filter(category_id=category_id)
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(parent_id=None)
        return context


class ProductImageView(TemplateView):
    model = ProductImage
    template_name = 'apps/product_detail.html'
    context_object_name = 'product_image'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'apps/product_detail.html'
    context_object_name = 'product'