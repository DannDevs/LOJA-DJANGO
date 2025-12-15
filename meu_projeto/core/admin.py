from django.contrib import admin
from .models import *

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nome')
    search_fields = ('codigo', 'nome')

@admin.register(Vendedor)
class VendedorAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nome')
    search_fields = ('codigo', 'nome')

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descricao', 'preco', 'quantidadeestoque')
    search_fields = ('codigo', 'descricao')

@admin.register(Venda)
class VendaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'cliente', 'vendedor', 'valor')
    search_fields = ('codigo',)

@admin.register(ItemVenda)
class ItemVendaAdmin(admin.ModelAdmin):
    list_display = ('venda', 'produto', 'quantidade', 'preco_unitario')

@admin.register(MovimentoItem)
class MovimentoItemAdmin(admin.ModelAdmin):
    list_display = ('tipomovimento', 'produto', 'qtdmovimento', 'preco')

@admin.register(Duplicata)
class DuplicataAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'venda', 'valor', 'tipo', 'pago')
    list_filter = ('tipo', 'pago')

@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'razaosocial', 'segmento')
    search_fields = ('codigo', 'razaosocial')

@admin.register(Entrada)
class EntradaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'fornecedor', 'valor')
