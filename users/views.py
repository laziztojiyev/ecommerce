from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import FormView, UpdateView, TemplateView, ListView

from apps.forms import UserRegistrationForm
from users.models import CustomUser
from users.tasks import sending_email


class RegisterView(FormView):
    form_class = UserRegistrationForm
    template_name = 'auth/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        sending_email.delay([form.data.get('email')])
        return super().form_valid(form)


class ProfileLoginView(TemplateView, LoginRequiredMixin):
    template_name = 'auth/user_settings.html'


class UserUpdateView(UpdateView):
    model = CustomUser
    fields = ['first_name', 'last_name', 'phone_number', 'about_me', 'email']
    template_name = 'auth/user_settings.html'
    success_url = reverse_lazy('login')

    def get_object(self, queryset=None):
        return self.request.user


class ChangePasswordView(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'auth/user_settings.html'
    success_url = reverse_lazy('login')

    def form_invalid(self, form):
        return super().form_invalid(form)


class LogoutView(ListView):
    model = CustomUser
    template_name = 'auth/logout.html'
    context_object_name = 'logout'
