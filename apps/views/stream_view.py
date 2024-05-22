from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import DetailView, FormView

from apps.forms import StreamModelForm
from apps.models.product_addings import Threads


class StreamListView(LoginRequiredMixin, FormView):
    template_name = 'apps/threads.html'
    form_class = StreamModelForm

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['streams'] = Stream.objects.filter(user=self.request.user)
    #     return context

    def form_valid(self, form):
        stream = form.save(commit=False)
        stream.user = self.request.user
        stream.save()
        return redirect('stream')

    def form_invalid(self, form):
        return super().form_invalid(form)


class StreamDetailView(DetailView):
    model = Threads
    template_name = 'apps/stream_detail.html'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        stream = get_object_or_404(Threads.objects.all(), pk=pk)
        return stream.product
