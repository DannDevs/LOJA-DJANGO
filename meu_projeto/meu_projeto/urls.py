"""
URL configuration for meu_projeto project.

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
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('vendedores/',views.vendedorview,name='vendedores'),
    path('vendedores/cadastro/',views.cadastro_vendedor,name='cadastrovendedor'),
    path('vendedores/<int:id>/edit/',views.editar_vendedor,name='editarvendedor'),
    path('vendedores/<int:id>/deletar/',views.vendedorremover,name='removervendedor'),
    path('clientes/',views.clienteview,name='clientes'),
    path('clientes/cadastro/',views.cadastro_cliente,name="cadastrocliente")
]
