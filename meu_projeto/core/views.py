from django.shortcuts import render,redirect,get_object_or_404
from .models import cliente,vendedor
from django.http import HttpResponse

# HOME PAGE

def home(request):


    return render(request, "home.html")

# VALIDADORES

def validacod(codigo):
    return vendedor.objects.filter(codigo=codigo).exists()
def validacodcliente(codigo):
    return cliente.objects.filter(codigo=codigo).exists()

# VENDEDORES

def editar_vendedor(request,id):
    erro = None

    vend = get_object_or_404(vendedor,id=id)

    if request.method == 'POST':    
        codigo = request.POST.get('codigo')
        nome = request.POST.get('nome')

        if validacod(codigo) == True and vend.codigo != codigo:
            erro = "Codigo Já Cadastrado"
        else:
            vend.codigo = codigo
            vend.nome = nome
            vend.save()
            return redirect('vendedores')
             

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


def clienteview(request):
    clientes = cliente.objects.all()
    return render(request,'clientes.html',{'clientes':clientes})


def cadastro_cliente(request):
    erro = None
    
    if request.method == "POST":
        codigo = request.POST.get("codigocliente")
        nome = request.POST.get("nomecliente")

        if validacodcliente(codigo) ==  True:
            erro = "Cliente ja cadastrado"
        else:
            cliente.objects.create(codigo=codigo,nome=nome)
            sucesso = "Cliente Cadastrado!"
    
    return render(request,'cadastro_cliente.html',
                  {"erro": erro }
                  )
    