from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import path, include




def logout_v(req):
    logout(req)
    return redirect('product_list')


urlpatterns = [
    path('admin/logout/', logout_v),
    path('admin/', admin.site.urls),
    path('', include('apps.urls')),
    path('auth/', include('users.urls'))
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
