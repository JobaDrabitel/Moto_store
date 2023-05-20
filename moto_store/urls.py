
from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from myapp.views import home
from django.urls import include
from myapp import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('myapp/', include('myapp.urls')),  # Добавьте эту строку
    path('', home, name='home'),
    path('drf/', include('drf.urls')),
    path('myapp/profile/', views.profile, name='profile'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('docs/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)