# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from .models import CustomUser


class UsersProxy(CustomUser):
    class Meta:
        proxy = True
        verbose_name = 'Foydalanuvchi'
        verbose_name_plural = 'Foylanuvchilar'


class OperatorProxy(CustomUser):
    class Meta:
        proxy = True
        verbose_name = 'operator'
        verbose_name_plural = 'operatorlar'


class MenegerProxy(CustomUser):
    class Meta:
        proxy = True
        verbose_name = 'menejer'
        verbose_name_plural = 'menejerlar'


class CurerProxy(CustomUser):
    class Meta:
        proxy = True
        verbose_name = 'Curer'
        verbose_name_plural = 'Curerlar'


class AdminProxy(CustomUser):
    class Meta:
        proxy = True

        verbose_name = 'Admin'
        verbose_name_plural = 'Adminlar'


class ConfiguredFields(BaseUserAdmin):
    list_display = ['username', 'first_name', 'last_name', 'is_staff', 'phone_number', 'about_me']

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'image', "type", 'phone_number', 'about_me')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide   ',),
            'fields': ('username', 'password1', 'password2', 'type', 'image', 'about_me', 'phone_number'),
        }),
    )


@admin.register(UsersProxy)
class UsersProxyAdmin(BaseUserAdmin):
    list_display = ['username', 'first_name']

    def get_queryset(self, request):
        return super().get_queryset(request).filter(type=CustomUser.Type.USERS)


@admin.register(OperatorProxy)
class OperatorProxyAdmin(ConfiguredFields):

    def get_queryset(self, request):
        return super().get_queryset(request).filter(type=CustomUser.Type.OPERATOR)


@admin.register(MenegerProxy)
class MenegerProxyAdmin(ConfiguredFields):

    def get_queryset(self, request):
        return super().get_queryset(request).filter(type=CustomUser.Type.MENEGER)


@admin.register(CurerProxy)
class CurerProxyAdmin(ConfiguredFields):

    def get_queryset(self, request):
        return super().get_queryset(request).filter(type=CustomUser.Type.KURYER)


@admin.register(AdminProxy)
class AdminProxyAdmin(ConfiguredFields):

    def get_queryset(self, request):
        return super().get_queryset(request).filter(type=CustomUser.Type.ADMIN)


@admin.register(CustomUser)
class UserAdmin(ConfiguredFields):
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)


admin.site.unregister(Group)
