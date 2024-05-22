from django.shortcuts import redirect
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, FormView
from django.db.models import Q, F
from apps.forms import OrderModelForm
from apps.models import Order, Product


# Create your views here.


class OrderView(FormView):
    form_class = OrderModelForm
    template_name = 'apps/product_detail.html'

    def form_valid(self, form):
        obj = form.save()
        return redirect(reverse('ordered', kwargs={'pk': obj.pk}))

    def form_invalid(self, form):
        return redirect(reverse('product_detail', kwargs={'pk': self.request.POST.get('product')}))


class OrderListView(ListView):
    paginate_by = 9
    model = Order
    queryset = Order.objects.order_by('-id')
    template_name = 'apps/orders_list.html'
    context_object_name = 'order_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item_count'] = self.get_queryset().count()
        return context


class OrderedView(DetailView):
    template_name = 'apps/success_page.html'
    model = Order
    context_object_name = 'order'


class OrderDetailView(DetailView):
    model = Order
    template_name = 'apps/order_product_detail.html'
    context_object_name = 'order_detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch the associated product for the order
        context['product'] = self.object.product
        return context



