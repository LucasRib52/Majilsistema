from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from .views import CustomLoginView, dashboard
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Página de login
    path('login/', CustomLoginView.as_view(), name='login'),

    # Logout
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    # Dashboard (após login)
    path('', dashboard, name='dashboard'),

    # Apps do sistema
    path('clientes/', include('clientes.urls')),
    path('honorarios/', include('honorarios.urls')),
    path('condominio/', include('condominio.urls')),
]

# 🚀 Adiciona suporte para servir arquivos de mídia no ambiente de desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
