"""
URL configuration for pawsathome project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from . import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    # path('sitters/', TemplateView.as_view(template_name='sitters.html'), name='sitters'),
    # path('pets/', TemplateView.as_view(template_name='pets.html'), name='pets'),
    path('accounts/', include('accounts.urls')),
    path('pets_sitting/', include('petsitting.urls')),
    # path('test-tailwind/', TemplateView.as_view(template_name='base.html'),
    #      name='test_tailwind'),
    path("__reload__/", include("django_browser_reload.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
