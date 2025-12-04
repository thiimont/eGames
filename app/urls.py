from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_usuario, name='login'),
    path('cadastro/', views.cadastro_usuario, name='cadastro'),
    path('perfil/', views.perfil_usuario, name='perfil'),
    path('logout/', views.logout_usuario, name='logout'),
    path('compra/<int:id_produto>', views.compra, name='compra'),
]