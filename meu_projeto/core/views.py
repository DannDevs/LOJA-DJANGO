from django.shortcuts import render,redirect
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

def vendedorview(request):
    # ------ LISTAR ---------
    vendedores = vendedor.objects.all()

    return render(request,'vendedores.html',{
        'vendedores':vendedores})

def vendedorremover(request):

    if request.method == "POST":

        id = request.POST.get("codigo")

        vendedor.objects.filter(id=id).delete()
        return redirect('vendedores')
    
    return render(request,'remover_vendedor.html')

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
    