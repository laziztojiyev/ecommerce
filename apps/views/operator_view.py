from apps.models import Order
from django.views.generic import ListView


class BaseOperatorListView(ListView):
    queryset = Order.objects.all()
    template_name = 'apps/../../templates/operators/operator.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return super().get_queryset().filter(status=Order.Status.NEW)
