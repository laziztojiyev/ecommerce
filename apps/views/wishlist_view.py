from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView

from apps.models import Wishlist


class WishlistView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        wishlist, created = Wishlist.objects.get_or_create(user=request.user, product_id=kwargs['product_id'])
        if not created:
            wishlist.delete()
        return redirect('product_list')


class WishlistShowView(ListView):
    model = Wishlist
    template_name = 'apps/wishlist_list.html'
    context_object_name = 'wishlists'


class WishlistRemoveView(View):
    def get(self, request, product_id):
        Wishlist.objects.filter(product_id=product_id, user_id=self.request.user.id).delete()
        return redirect(reverse('wishlist_list'))