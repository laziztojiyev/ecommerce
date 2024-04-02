from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.urls import path

from users.views import RegisterView, ProfileLoginView, UserUpdateView, ChangePasswordView, LogoutView




urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='auth/login.html', next_page='product_list'), name='login'),
    path('settings/', ProfileLoginView.as_view(), name='profile'),
    path('settings/update/', UserUpdateView.as_view(), name='user_update'),
    path('settings/update_password/', ChangePasswordView.as_view(), name='change_password'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

