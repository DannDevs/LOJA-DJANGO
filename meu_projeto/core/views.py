from django.shortcuts import render,redirect,get_object_or_404
from .models import cliente,vendedor,produto
from django.http import HttpResponse

# HOME PAGE

def home(request):


    return render(request, "home.html")

# VALIDADORES

def validacod(codigo):
    return vendedor.objects.filter(codigo=codigo).exists()
def validacodcliente(codigo):
    return cliente.objects.filter(codigo=codigo).exists()
def validacodproduto(codigo):
    return produto.objects.filter(codigo=codigo).exists()

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
             
    return render(request,'editarvendedor.html',
    {'vend':vend,'erro':erro}
    )

def vendedorview(request):
    # ------ LISTAR ---------
    vendedores = vendedor.objects.all()

    return render(request,'vendedores.html',{
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
    return render(request,'cadastro_vendedor.html',
                  {"erro":erro})

# CLIENTE VIEW

def clienteview(request):
    clientes = cliente.objects.all()
    return render(request,'clientes.html',{'clientes':clientes})

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
        
    return render(request,'editarcliente.html',{'cli':cli,'erro':erro})

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
    
    return render(request,'cadastro_cliente.html',
                  {"erro": erro }
                  )

# ------ PRODUTOS ------

def produtoview(request):
    produtos = produto.objects.all()

    return render(request,'produtos.html',{'produtos':produtos})

def cadastro_produto(request):
    if request.method == 'POST':
        codigo = request.POST.get("codigo")
        descricao = request.POST.get("descricao")
        
    return render(request,'cadastro_produto.html')
    
    