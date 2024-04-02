import time

from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView, FormView, TemplateView
from django.core.mail import send_mail
from apps.forms import OrderModelForm
from apps.models import Product, Wishlist, ProductImage, Order, Category
from apps.tasks import add
from root.settings import EMAIL_HOST_USER


# Create your views here.
class ProductListView(ListView):
    model = Product
    template_name = 'apps/product grid.html'
    context_object_name = 'products'
    paginate_by = 9

    def get_queryset(self):
        category_id = self.request.GET.get('category', None)
        if category_id:
            return self.queryset.filter(category_id=category_id)
        return super().get_queryset()

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
        add.delay(5)  # celery
        # send_mail(subject, message, EMAIL_HOST_USER, [recipient_list])
        end = time.time()
        return HttpResponse(f'saytga yuborildi{end - start}')


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


class WishlistView(View):
    def get(self, request, *args, **kwargs):
        wishlist, created = Wishlist.objects.get_or_create(user=request.user, product_id=kwargs['product_id'])
        if not created:
            wishlist.delete()
        return redirect('product_list')


class OrderView(FormView):
    form_class = OrderModelForm
    template_name = 'apps/product_detail.html'

    def form_valid(self, form):
        obj = form.save()
        return redirect(reverse('ordered', kwargs={'pk': obj.pk}))

    def form_invalid(self, form):
        return redirect(reverse('product_detail', kwargs={'pk': self.request.POST.get('product')}))


class OrderedView(DetailView):
    template_name = 'apps/ordered.html'
    model = Order
    context_object_name = 'order'


class WishlistShowView(ListView):
    model = Wishlist
    template_name = 'apps/wishlist_list.html'
    context_object_name = 'wishlists'


class WishlistRemoveView(View):
    def get(self, request, product_id):
        Wishlist.objects.filter(product_id=product_id, user_id=self.request.user.id).delete()
        return redirect(reverse('wishlist_list'))
