from django.shortcuts import render,redirect,get_object_or_404
from .models import cliente,vendedor,produto
from django.http import HttpResponse

# HOME PAGE

def home(request):


    return render(request, "views/home.html")

# VALIDADORES

def validacod(codigo):
    return vendedor.objects.filter(codigo=codigo).exists()
def validacodcliente(codigo):
    return cliente.objects.filter(codigo=codigo).exists()
def validacodproduto(codigo):
    return produto.objects.filter(codigo=codigo).exists()
def validaquantidade(quantidade):
    return quantidade > -1

# VENDEDORES

def editar_vendedor(request,id):
    erro = None

    vend = get_object_or_404(vendedor,id=id)

    if request.method == 'POST':    
        codigo = request.POST.get('codigo')
        nome = request.POST.get('nome')

        if validacod(codigo) == False and vend.codigo != codigo:  
            vend.codigo = codigo
            vend.nome = nome
            vend.save()
            
            return redirect('vendedores')
        else:
            erro = "Codigo Já Cadastrado"
             
    return render(request,'edicao/editarvendedor.html',
    {'vend':vend,'erro':erro}
    )

def vendedorview(request):
    # ------ LISTAR ---------
    vendedores = vendedor.objects.all()

    return render(request,'modelos/vendedores.html',{
        'vendedores':vendedores})

#  ------------ REMOVER ------------

def vendedorremover(request,id):

    vendedor.objects.filter(id=id).delete()
    return redirect('vendedores')
    

def cadastro_vendedor(request):
    erro = None

    if request.method == "POST":
        codigo = request.POST.get("codigo")
        nome = request.POST.get("nome")

        if not codigo or not nome:
            erro = "Preencha Corretamente os campos"
        
        if validacod(codigo) == True:
            erro = "Codigo ja cadastrado"
        
        else:

            vendedor.objects.create(codigo=codigo,nome=nome)
            return redirect('vendedores')
    return render(request,'cadastros/cadastro_vendedor.html',
                  {"erro":erro})

# CLIENTE VIEW

def clienteview(request):
    clientes = cliente.objects.all()
    return render(request,'modelos/clientes.html',{'clientes':clientes})

# ------ EDIÇAO CLIENTE -------

def editar_cliente(request,id):
    erro = None
    cli = get_object_or_404(cliente,id=id)

    if request.method == "POST":
        codigo = request.POST.get('codigo')
        nome = request.POST.get('nome')
        if validacod(codigo) == False and codigo != cli.codigo:
            cli.codigo = codigo
            cli.nome = nome
            cli.save()
            return redirect('clientes')
        else:
            erro = "Erro ao cadastrar"
        
    return render(request,'edicao/editarcliente.html',{'cli':cli,'erro':erro})

# ---------- REMOVER CLIENTE ----

def remover_cliente(request,id):
    cliente.objects.filter(id=id).delete()
    return redirect('clientes')

# ------ CADASTRO CLIENTE ----

def cadastro_cliente(request):
    erro = None
    
    if request.method == "POST":
        codigo = request.POST.get("codigocliente")
        nome = request.POST.get("nomecliente")

        if validacodcliente(codigo) ==  True:
            erro = "Cliente ja cadastrado"
        else:
            cliente.objects.create(codigo=codigo,nome=nome)
            return redirect('clientes')
    
    return render(request,'cadastros/cadastro_cliente.html',
                  {"erro": erro }
                  )

# ------ PRODUTOS ------

def produtoview(request):
    produtos = produto.objects.all()

    return render(request,'modelos/produtos.html',{'produtos':produtos})

def cadastro_produto(request):
    erro = None

    if request.method == 'POST':
        codigo = request.POST.get("codigo")
        if validacodproduto(codigo) == False:
            descricao = request.POST.get("descricao")
            preco = request.POST.get("preco")
            quantidade = int(request.POST.get("quantidade"))
            if validaquantidade(quantidade) == True:
                produto.objects.create(codigo=codigo,descricao=descricao,preco=preco,quantidadeestoque=quantidade)
                return redirect('produtos')
            else:
                erro = "Quantidade invalida"
        else:
            erro = "Codigo ja foi cadastrado"
                
      
        
    return render(request,'cadastros/cadastro_produto.html',{'erro':erro})

# ----- EDITAR PRODUTO ------
def editar_produto(request,id):
    erro = None
    prod = produto.objects.get(id=id)

    if request.method == 'POST':
        codigo = request.POST.get("codigo")
        descricao = request.POST.get("descricao")
        preco = request.POST.get("preco")

        if validacodproduto(codigo) == False and codigo != prod.codigo:
            prod.codigo = codigo
            prod.descricao = descricao
            prod.preco = preco
            prod.save()
            return redirect('produtos')
        else:
            erro = "Codigo ja cadastrado!" 
    
    return render(request,'edicao/editarproduto.html',{'prod':prod,'erro':erro})

# ------- REMOVER PRODUTO -------

def remover_produto(request,id):
    produto.objects.get(id=id).delete()
    return redirect('produtos')

def vendaview(request):
    return render(request,'modelos/vendas.html')
    