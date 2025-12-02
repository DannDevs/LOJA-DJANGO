from django.shortcuts import render,redirect,get_object_or_404
from .models import cliente,vendedor,produto,venda,movimentoitem
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
def validacodvenda(codigo):
    return venda.objects.filter(codigo=codigo).exists()
def produtoexiste(id):
    return produto.objects.filter(id=id).exists()

# VENDEDORES

def editar_vendedor(request,id):
    erro = None

    vend = get_object_or_404(vendedor,id=id)

    if request.method == 'POST':    
        codigo = int(request.POST.get('codigo'))
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
        codigo = int(request.POST.get("codigo"))
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
        codigo = int(request.POST.get('codigo'))
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
        codigo = int(request.POST.get("codigocliente"))
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
        codigo = int(request.POST.get("codigo"))
        if validacodproduto(codigo) == False:
            descricao = request.POST.get("descricao")
            preco = request.POST.get("preco")
            quantidade = int(request.POST.get("quantidade"))
            if validaquantidade(quantidade) == True:
                produto.objects.create(codigo=codigo,descricao=descricao,preco=preco,quantidadeestoque=quantidade)
                movimentoitem.objects.create()

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
        codigo = int(request.POST.get("codigo"))
        descricao = request.POST.get("descricao")
        preco = request.POST.get("preco")

        print(codigo)
        print(prod.codigo)
        print(validacodproduto(codigo))
        if validacodproduto(codigo) == False or codigo == prod.codigo:
            prod.codigo = codigo
            prod.descricao = descricao
            prod.preco = preco
            prod.save()
            return redirect('produtos')
        else:
            erro = "Codigo ja cadastrado!" 
    
    return render(request,'edicao/editarproduto.html',{'prod':prod,'erro':erro})


# --------- AJUSTAR ESTOQUE

def ajustar_estoque(request,id):
    
    prod = produto.objects.get(id=id)


    estoque = request.POST.get("estoque")

    if validacodproduto(prod.codigo) == True:
        pass

    return render(request,'edicao/editarestoque.html',{'prod':prod})



# ------- REMOVER PRODUTO -------

def remover_produto(request,id):
    produto.objects.get(id=id).delete()
    return redirect('produtos')

# ------- VENDAS VIEW -------

def vendaview(request):

    vendas = venda.objects.all()

    return render(request,'modelos/vendas.html',{'vendas':vendas})

def gerar_venda(request):

    cliente_padrao, _ = cliente.objects.get_or_create(
        id = 0,
        defaults={'codigo':0,'nome':"CLIENTE PADRÃO"}
    )

    vendedor_padrao, _ = vendedor.objects.get_or_create(
        id = 0,
        defaults={'codigo':0,'nome':"VENDEDOR PADRÃO"}
    )

    nova_venda = venda.objects.create(
        codigo = 0,
        cliente= cliente_padrao,
        vendedor= vendedor_padrao,
        valor= 0
        )

    return redirect('cadastrovenda',id=nova_venda.id)
    
def cadastro_venda(request,id):

    ven_atual = get_object_or_404(venda,id=id)

    clientes = cliente.objects.all()
    vendedores = vendedor.objects.all()
    produtos = produto.objects.all()

    valor_total = 0
    erro = None
    cli = None
    ven = None

    if request.method == 'POST' and "add_item_apos" in request.POST:
        produto_id = request.POST.get("produto")
        preco_unitario = request.POST.get("preco_unitario")
        quantidade = request.POST.get('quantidade')

        prod = produto.objects.get(id=produto_id)

        if produtoexiste(prod.id) == True:
            print(request.POST)
            itemvenda.objects.create(
                venda=ven_atual,
                produto=prod,
                quantidade=quantidade,
                preco_unitario=preco_unitario
            )
            return redirect('cadastrovenda',id=id)
        else:
            erro = "Produto não existe"
            
    if request.method == 'POST' and "add_venda" in request.POST:   
        codigo = ven_atual.codigo
        cliente_id = ven_atual.cliente.id
        vendedor_id = ven_atual.vendedor.id

        itensvenda = itemvenda.objects.filter(venda = ven_atual)

        
        for valor in itensvenda:
            
            valor_total += valor.preco_unitario * valor.quantidade

        cli = get_object_or_404(cliente,id=cliente_id)
        ven = get_object_or_404(vendedor,id=vendedor_id)
        if validacodvenda(codigo) == True:
            if validacodcliente(cli.codigo) == True:
                if validacod(ven.codigo) == True:
                    
                    ven_atual.valor = valor_total    
                    ven_atual.save()                    
                    return redirect('vendas')
                else:
                    erro = "Codigo Vendedor Nao Existe"
            else:
                erro = "Codigo Cliente nao existe"    
        else:
            erro = "Codigo Venda ja utilizado"
            
    
    # -------------- ADD PRODUTO ------------
          
    if request.method == 'POST' and "add_item" in request.POST:
        
        erroitem = None

        venda_atual = get_object_or_404(venda,id=id)
    
        codigo = int(request.POST.get('codigo'))
        cliente_id = request.POST.get('cliente')
        vendedor_id = request.POST.get('vendedor')

        produto_id = request.POST.get('produto')
        produtoadd = produto.objects.get(id=produto_id)

        quantidade = request.POST.get('quantidade')
        preco_unitario = request.POST.get('preco_unitario')

        cli = get_object_or_404(cliente,id=cliente_id)
        ven = get_object_or_404(vendedor,id=vendedor_id)

        if produtoexiste(produto_id) == True:
            if validacodvenda(codigo) == False:
                if validacodcliente(cli.codigo) == True:
                    if validacod(ven.codigo) == True: 
                    
                        itemvenda.objects.create(venda=venda_atual,produto=produtoadd,quantidade=quantidade,preco_unitario=preco_unitario)
                        
                        item = itemvenda.objects.get(venda=venda_atual)

                        ven_atual.codigo = codigo
                        ven_atual.cliente = cli
                        ven_atual.vendedor = ven
                        ven_atual.valor += item.preco_unitario * item.quantidade
                        ven_atual.save()

                        return redirect('cadastrovenda', id=id)
                        
                    else:
                        erro = "Codigo Vendedor Nao Existe"
                else:
                    erro = "Codigo Cliente nao existe"    
            else:
                erro = "Codigo Venda ja utilizado"
        else:
            erroitem = "Produto nao Existe"
            return redirect('cadastrovenda')
        
    return render(request,'cadastros/cadastro_venda.html',{
        'cli':cli,
        'ven':ven,
        'clientes':clientes,
        'vendedores':vendedores,
        'produtos':produtos,
        'erro':erro,
        'ven_atual':ven_atual,
        'itensvenda':itemvenda.objects.filter(venda = ven_atual)
        })

def remover_venda(request,id):
    venda.objects.get(id=id).delete( )
    return redirect('vendas')




    

    
    

        