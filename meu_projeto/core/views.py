from django.shortcuts import render,redirect,get_object_or_404
from .models import Cliente,Vendedor,Produto,Venda,MovimentoItem,ItemVenda,Duplicata
from django.http import HttpResponse
from django.db.models import Sum,Value,DecimalField
from django.db.models.functions import Coalesce
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login,logout
from django.contrib.auth.decorators import login_required
# HOME PAGE

@login_required
def home(request):

    numeroclientes = Cliente.objects.count()

    receita = Duplicata.objects.aggregate(receita=Coalesce(
        Sum('valor'), 
        Value(0),
        output_field=DecimalField())
        )['receita']
    quantidadevenda = Venda.objects.count()


    return render(request, "views/home.html",{
        'numeroclientes':numeroclientes,
        'receita':receita,
        'quantidadevenda':quantidadevenda
        })

# VALIDADORES

def validacod(codigo):
    return Vendedor.objects.filter(codigo=codigo).exists()
def validacodcliente(codigo):
    return Cliente.objects.filter(codigo=codigo).exists() 
def validacodproduto(codigo): 
    return Produto.objects.filter(codigo=codigo).exists()
def validaquantidade(quantidade):
    return quantidade > -1
def validacodvenda(codigo):
    return Venda.objects.filter(codigo=codigo).exists()
def produtoexiste(id):
    return Produto.objects.filter(id=id).exists()
def temduplicata(id):
    return Duplicata.objects.filter(venda_id=id).exists()
def validacodigo(codigo):
    return codigo >= 1
def verificaestoque(codigo,quantidade):
    produto = Produto.objects.get(codigo=codigo)
    quantidadevalida = int(quantidade)
    return produto.quantidadeestoque >= quantidadevalida

# ----- LOGIN ---------

def login_view(request):
    erro = None
    if request.method == 'POST':
        usuario = request.POST.get('username')
        senha = request.POST.get('password')

        if not senha or not usuario:
            erro = 'Preencha todos os campos'
        else: 
            user = authenticate(request,username=usuario,password=senha)
            if user is not None:
                auth_login(request,user)
                return redirect('home')
            else:
                erro = 'Usuario ou senha invalidas'
    return render(request,'views/login.html',{'erro':erro})

# VENDEDORES
@login_required
def editar_vendedor(request,id):
    erro = None

    vend = get_object_or_404(Vendedor,id=id)

    if request.method == 'POST':    
        codigo = int(request.POST.get('codigo'))
        nome = request.POST.get('nome')

        if validacod(codigo) == True and vend.codigo == codigo:  
            vend.codigo = codigo
            vend.nome = nome
            vend.save()
            
            return redirect('vendedores')
        else:
            erro = "Codigo Já Cadastrado"
             
    return render(request,'edicao/editarvendedor.html',
    {'vend':vend,'erro':erro}
    )
@login_required
def vendedorview(request):
    # ------ LISTAR ---------
    vendedores = Vendedor.objects.all()

    return render(request,'modelos/vendedores.html',{
        'vendedores':vendedores})


#  ------------ REMOVER ------------
@login_required
def vendedorremover(request,id):

    Vendedor.objects.filter(id=id).delete()
    return redirect('vendedores')
    
@login_required
def cadastro_vendedor(request):
    erro = None

    if request.method == "POST":
        codigo = int(request.POST.get("codigo"))
        nome = request.POST.get("nome")

        if not codigo or not nome:
            erro = "Preencha Corretamente os campos"
        
        if validacod(codigo) == False and validacodigo(codigo) == True:
            Vendedor.objects.create(codigo=codigo,nome=nome)
            return redirect('vendedores')
        else:
            erro = "Codigo ja cadastrado ou Invalido"
    return render(request,'cadastros/cadastro_vendedor.html',
                  {"erro":erro})

# CLIENTE VIEW
@login_required
def clienteview(request):
    clientes = Cliente.objects.all()
    return render(request,'modelos/clientes.html',{'clientes':clientes})

# ------ EDIÇAO CLIENTE -------
@login_required
def editar_cliente(request,id):
    erro = None
    cli = get_object_or_404(Cliente,id=id)

    if request.method == "POST":
        codigo = int(request.POST.get('codigo'))
        nome = request.POST.get('nome')
        if validacod(codigo) == True and codigo == cli.codigo:
            cli.codigo = codigo
            cli.nome = nome
            cli.save()
            return redirect('clientes')
        else:
            erro = "Erro ao cadastrar"
        
    return render(request,'edicao/editarcliente.html',{'cli':cli,'erro':erro})

# ---------- REMOVER CLIENTE ----
@login_required
def remover_cliente(request,id):
    Cliente.objects.filter(id=id).delete()
    return redirect('clientes')

# ------ CADASTRO CLIENTE ----
@login_required
def cadastro_cliente(request):
    erro = None
    
    if request.method == "POST":
        codigo = int(request.POST.get("codigocliente"))
        nome = request.POST.get("nomecliente")

        if validacodcliente(codigo) ==  True:
            erro = "Cliente ja cadastrado"
        else:
            Cliente.objects.create(codigo=codigo,nome=nome)
            return redirect('clientes')
    
    return render(request,'cadastros/cadastro_cliente.html',
                  {"erro": erro }
                  )

# ------ PRODUTOS ------
@login_required
def produtoview(request):
    produtos = Produto.objects.all()

    return render(request,'modelos/produtos.html',{'produtos':produtos})
@login_required
def cadastro_produto(request):
    erro = None

    if request.method == 'POST':
        codigo = int(request.POST.get("codigo"))
        if validacodproduto(codigo) == False:
            descricao = request.POST.get("descricao")
            preco = request.POST.get("preco")
            quantidade = int(request.POST.get("quantidade"))
            if validaquantidade(quantidade) == True:
                Produto.objects.create(codigo=codigo,descricao=descricao,preco=preco,quantidadeestoque=quantidade)
              

                return redirect('produtos')
            else:
                erro = "Quantidade invalida"
        else:
            erro = "Codigo ja foi cadastrado"
                
      
        
    return render(request,'cadastros/cadastro_produto.html',{'erro':erro})

# ----- EDITAR PRODUTO ------
@login_required
def editar_produto(request,id):
    erro = None
    prod = Produto.objects.get(id=id)

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
@login_required
def ajustar_estoque(request,id):
    erro  = None    
    quantidademov = 0
    preco_unitario = 0
    
    prod = Produto.objects.get(id=id)
    preco = request.POST.get("precoalt")
    quantidadeestoque = request.POST.get("estoquealt")
    tipomov = request.POST.get("tipomov")

    
    if quantidadeestoque is not None:
        quantidademov = int(quantidadeestoque)
    if preco is not None:
        preco_unitario = int(preco)

    if request.method == 'POST':
        if validacodproduto(prod.codigo) == True:
            print(tipomov)
            if tipomov == '1':
                if quantidademov >= 0:

                    preco_unitario = 0
                    prod.quantidadeestoque += quantidademov
                    prod.save()

                    MovimentoItem.objects.create(tipomovimento='+',produto=prod,qtdmovimento=quantidademov,preco=preco_unitario)
                    erro = " "

            if tipomov == '2':
                print('EROOOO')
                if quantidademov >= 0:
                    
                    preco_unitario = 0
                    prod.quantidadeestoque -= quantidademov
                    prod.save()

                    MovimentoItem.objects.create(tipomovimento='-',produto=prod,qtdmovimento=quantidademov,
                    preco=preco_unitario)
                    erro = " "

            if tipomov == '3':
                if preco_unitario >= 0: 
                    
                    quantidademov = 0
                    prod.preco = preco_unitario
                    prod.save()

                    MovimentoItem.objects.create(tipomovimento='$',produto=prod,qtdmovimento=quantidademov,preco=preco_unitario)

                    erro = " "
        else:
            erro =  "Produto nao foi cadastrado"

    return render(request,'edicao/editarestoque.html',{
        'prod':prod,
        'erro':erro,
        'mvto':MovimentoItem.objects.filter(produto_id=id)})


# ------- REMOVER PRODUTO -------
@login_required
def remover_produto(request,id):
    Produto.objects.get(id=id).delete()
    return redirect('produtos')

# ------- VENDAS VIEW -------
@login_required
def vendaview(request):

    vendas = Venda.objects.all()

    return render(request,'modelos/vendas.html',{'vendas':vendas})

@login_required
def gerar_venda(request):

    cliente_padrao, _ = Cliente.objects.get_or_create(
        id = 0,
        defaults={'codigo':0,'nome':"CLIENTE PADRÃO"}
    )

    vendedor_padrao, _ = Vendedor.objects.get_or_create(
        id = 0,
        defaults={'codigo':0,'nome':"VENDEDOR PADRÃO"}
    )

    nova_venda = Venda.objects.create(
        codigo = 0,
        cliente= cliente_padrao,
        vendedor= vendedor_padrao,
        valor= 0
        )

    return redirect('cadastrovenda',id=nova_venda.id)

@login_required
def cadastro_venda(request,id):

    ven_atual = get_object_or_404(Venda,id=id)

    clientes = Cliente.objects.all()
    vendedores = Vendedor.objects.all()
    produtos = Produto.objects.all()

    valor_total = 0
    erro = None
    sucesso = None
    cli = None
    ven = None

    if request.method == 'POST' and "add_item_apos" in request.POST:
        produto_id = request.POST.get("produto")
        preco_unitario = request.POST.get("preco_unitario")
        quantidade = request.POST.get('quantidade')

        prod = Produto.objects.get(id=produto_id)

        if produtoexiste(prod.id) == True:
            if verificaestoque(prod.codigo,quantidade):
                ItemVenda.objects.create(
                    venda=ven_atual,
                    produto=prod,
                    quantidade=quantidade,
                    preco_unitario=preco_unitario
                )

                item = ItemVenda.objects.get(venda=ven_atual,produto=prod)

                item.produto.quantidadeestoque -= item.quantidade
                item.produto.save()
                
                MovimentoItem.objects.create(
                    tipomovimento='-',    
                    produto=prod,
                    qtdmovimento =quantidade ,
                    preco =preco_unitario
                )
                return redirect('cadastrovenda',id=id)
            else:
                erro="Quantidade insuficiente"
                
        else:
            erro = "Produto não existe"
            
    if request.method == 'POST' and "add_venda" in request.POST:   
        codigo = ven_atual.codigo
        cliente_id = ven_atual.cliente.id
        vendedor_id = ven_atual.vendedor.id

        itensvenda = ItemVenda.objects.filter(venda = ven_atual)

        
        for valor in itensvenda:
            
            valor_total += valor.preco_unitario * valor.quantidade

        cli = get_object_or_404(Cliente,id=cliente_id)
        ven = get_object_or_404(Vendedor,id=vendedor_id)
        if validacodvenda(codigo) == True:
            if validacodcliente(cli.codigo) == True:
                if validacod(ven.codigo) == True:
                    if temduplicata(id) == True:
                        
                        duplicatavenda = Duplicata.objects.get(venda_id=id)

                        duplicatavenda.valor = ven_atual.valor

                        duplicatavenda.save()        
                        
                        ven_atual.valor = valor_total    
                        ven_atual.save()                    
                        return redirect('vendas')
                    else:
                        ven_atual.valor = valor_total    
                        ven_atual.save()   

                        Duplicata.objects.create(cliente=ven_atual.cliente,venda=ven_atual,valor=ven_atual.valor,tipo='R',pago='E')

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

        venda_atual = get_object_or_404(Venda,id=id)
    
        codigo = int(request.POST.get('codigo'))
        cliente_id = request.POST.get('cliente')
        vendedor_id = request.POST.get('vendedor')

        produto_id = request.POST.get('produto')
        produtoadd = Produto.objects.get(id=produto_id)

        quantidade = request.POST.get('quantidade')
        preco_unitario = request.POST.get('preco_unitario')

        cli = get_object_or_404(Cliente,id=cliente_id)
        ven = get_object_or_404(Vendedor,id=vendedor_id)

        if produtoexiste(produto_id) == True:
            if validacodvenda(codigo) == False:
                if validacodcliente(cli.codigo) == True:
                    if validacod(ven.codigo) == True: 
                        if verificaestoque(produtoadd.codigo,quantidade):
                    
                            ItemVenda.objects.create(venda=venda_atual,produto=produtoadd,quantidade=quantidade,preco_unitario=preco_unitario)

                            MovimentoItem.objects.create(
                            tipomovimento='-',    
                            produto=produtoadd,
                            qtdmovimento =quantidade ,
                            preco =preco_unitario
                            )
                            
                            item = ItemVenda.objects.get(venda=venda_atual)
                            item.produto.quantidadeestoque -= item.quantidade
                            item.produto.save()

                            ven_atual.codigo = codigo
                            ven_atual.cliente = cli
                            ven_atual.vendedor = ven
                            ven_atual.valor += item.preco_unitario * item.quantidade
                            ven_atual.save()
                            return redirect('cadastrovenda', id=id)
                        else:
                            erro = "Produto nao possui estoque"
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
        'sucesso':sucesso,
        'ven_atual':ven_atual,
        'itensvenda':ItemVenda.objects.filter(venda = ven_atual)
        })
@login_required
def remover_venda(request,id):
    Venda.objects.get(id=id).delete()
    return redirect('vendas')

# ------- DUPLICATAS -----
@login_required
def duplicataview(request):
    duplicatas = Duplicata.objects.all()

    return render(request,'modelos/duplicata.html',{'duplicatas':duplicatas})
@login_required
def excluir_duplicata(request,id):

    Duplicata.objects.get(id=id).delete

    return redirect('duplicatas')
@login_required
def estoqueview(request):

    estoque = MovimentoItem.objects.all()

    return render(request,'modelos/estoque.html',{'estoque':estoque})
@login_required
def remover_item(request,venid,id):
    ItemVenda.objects.get(id=id).delete()
    return redirect('cadastrovenda',id=venid)
@login_required
def remover_baixa(request,id):
    erro = None
    dup = Duplicata.objects.get(id=id)

    if dup.pago == 'P':
        dup.pago = 'E'
        dup.save()
        return redirect('duplicatas')
    else:
        erro = 'Duplicata Nao Possui Baixa'
    return redirect('duplicatas')
@login_required 
def baixar_duplicata(request,id):
    erro = None
    dup = Duplicata.objects.get(id=id)
    
    if dup.pago == 'E' or dup.pago == 'A':
        dup.pago = 'P'
        dup.save()
        return redirect('duplicatas')
    else:
        erro = "Duplicata Já Foi Baixada"
    return redirect('duplicatas')


def logout_view(request):
    logout(request)
    return redirect('login')




    

    
    

        