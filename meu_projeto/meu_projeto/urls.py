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
    path('clientes/cadastro/',views.cadastro_cliente,name="cadastrocliente"),
    path('clientes/<int:id>/edit/',views.editar_cliente,name='editarcliente'),
    path('clientes/<int:id>/deletar/',views.remover_cliente,name='removercliente'),
    path('produtos/',views.produtoview,name='produtos'),
    path('produtos/cadastro',views.cadastro_produto,name='cadastroproduto'),
    path('produtos/<int:id>/edit/',views.editar_produto,name='editarproduto'),
    path('produtos/<int:id>/excluir/',views.remover_produto,name='removerproduto'),
    path('produtos/<int:id>/ajuste/',views.ajustar_estoque,name='ajustarestoque'),
    path('venda/',views.vendaview,name='vendas'),
    path('venda/gerarvenda/',views.gerar_venda,name='gerarvenda'),
    path('venda/cadastro/<int:id>',views.cadastro_venda,name='cadastrovenda'),
    path('venda/<int:id>/deletar/',views.remover_venda,name='removervenda'),
    # path('venda/additem/<int:vendaid>',views.add_item_venda,name='additemvenda'),
    path('duplicatas/',views.duplicataview,name='duplicatas')
]
