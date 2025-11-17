from django.shortcuts import render,redirect
from .models import cliente,vendedor
from django.http import HttpResponse

def home(request):


    return render(request, "home.html")

def validacod(codigo):
    return vendedor.objects.filter(codigo=codigo).exists()
def validacodcliente(codigo):
    return cliente.objects.filter(codigo=codigo).exists()

def vendedor(request):
    erro = None

    if request.method == "POST":
        codigo = request.POST.get("codigo")
        nome = request.POST.get("nome")

        if not codigo or not nome:
            erro = "Preencha Corretamente os campos"
        
        if validacod(codigo) == True:
            erro = "Codigo ja cadastrado"
        
        else:

            if codigo == "":
                codigo = 0
            
            vendedor.objects.create(codigo=codigo,nome=nome)
            return redirect('/')
    return render(request,'vendedores.html',
                  {"erro":erro})


def clienteview(request):
    clientes = cliente.objects.all()
    return render(request,'clientes.html',{'clientes':clientes})


def cadastro_cliente(request):
    erro = None
    
    if request.method == "POST":
        codigo = request.POST.get("codigo")
        nome = request.POST.get("nome")

        if validacodcliente(codigo) ==  True:
            erro = "Cliente ja cadastrado"
        else:
            cliente.objects.create(codigo=codigo,nome=nome)
            return redirect('cliente')
    
    return render(request,'cadastro_cliente.html')
    