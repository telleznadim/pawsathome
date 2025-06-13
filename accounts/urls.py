from django.urls import path
from .views import login_view, editprofile_view
from .views import RegisterView
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', login_view, name='login'),
    path('editprofile/', editprofile_view, name='profile'),
    path('logout/', LogoutView.as_view(template_name="accounts/templates/logout.html"), name='logout'),
    path('agregar_Avatar/', views.agregarAvatar, name="agregar_Avatar")
]
