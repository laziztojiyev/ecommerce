from django.urls import path

from apps.views import ProductListView, ProductDetailView, WishlistView, OrderView, OrderedView, \
    WishlistShowView, WishlistRemoveView, MarketListView, SendMailView, FilteredCategoriesListView, StreamListView, \
    StreamDetailView, OrderListView, OrderDetailView
from apps.views.operator_view import BaseOperatorListView

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('product-detail/<str:slug>', ProductDetailView.as_view(), name='product_detail'),
    path('market/', MarketListView.as_view(), name='market'),
    path('category/<int:pk>', ProductListView.as_view(), name='products_list'),
    path('category', FilteredCategoriesListView.as_view(), name='categories_list'),
    path('send_mails/', SendMailView.as_view(), name='send'),
    path('wishlist/add/<int:product_id>', WishlistView.as_view(), name='wishlist_create'),
    path('order', OrderView.as_view(), name='order'),
    path('ordered_list', OrderListView.as_view(), name='ordered_list'),
    path('ordered/<int:pk>', OrderedView.as_view(), name='ordered'),
    path('ordered_detail/<int:pk>', OrderDetailView.as_view(), name='ordered_detail'),
    path('liking', WishlistShowView.as_view(), name='wishlist_list'),
    path('liking/delete/<int:product_id>', WishlistRemoveView.as_view(), name='deleting_wishlist'),
    path('stream/', StreamListView.as_view(), name='stream'),
    path('stream/<int:pk>/', StreamDetailView.as_view(), name='stream_detail'),
]


urlpatterns += [
    path('operator/new/', BaseOperatorListView.as_view(), name='orders_list'),
]