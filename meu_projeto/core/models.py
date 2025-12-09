from django.db import models

class Cliente(models.Model):
    codigo = models.IntegerField()
    nome = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.codigo} - {self.nome}"
    
class Vendedor(models.Model):
    codigo = models.IntegerField()
    nome = models.CharField(max_length=100)

    def __str__(self):
        return f" {self.codigo} - {self.nome}"
    
class Produto(models.Model):
    codigo = models.IntegerField()
    descricao = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10,decimal_places=2)
    unidade = models.CharField(max_length=2,default="UN")
    quantidadeestoque = models.DecimalField(max_digits=10,decimal_places=2,default=0)

    def __str__(self):
        return f"{self.codigo} - {self.descricao}"

class Venda(models.Model):
    codigo = models.IntegerField()
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    vendedor = models.ForeignKey(Vendedor, on_delete=models.PROTECT)
    valor = models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return f"{self.codigo}"

class ItemVenda(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    quantidade = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    preco_unitario = models.DecimalField(max_digits=10,decimal_places=2,default=0)

    def __str__(self):
        return f"{self.produto}"

class MovimentoItem(models.Model):

    MOVIMENTO_CHOICES = [
        ('+','ENTRADA'),
        ('-','SAIDA'),
        ('$','CUSTO')
    ]

    tipomovimento = models.CharField(max_length=1,choices=MOVIMENTO_CHOICES) 
    produto = models.ForeignKey(Produto,on_delete=models.CASCADE)
    qtdmovimento = models.DecimalField(max_digits=8,decimal_places=2,default=0)
    preco = models.DecimalField(max_digits=8,decimal_places=2,default=0)

class Duplicata(models.Model):

    TIPO_CHOICES = [
        ('P','PAGAR'),
        ('R','RECEBER'),
    ]

    PAGO_CHOICES = [
        ('P','PAGO'),
        ('E','EM ABERTO'),
        ('A','ATRASADO'),
    ]   

    cliente = models.ForeignKey(Cliente,on_delete=models.CASCADE)
    venda = models.ForeignKey(Venda,on_delete=models.CASCADE)
    valor = models.DecimalField(decimal_places=2,max_digits=8)
    tipo = models.CharField(max_length=1,choices=TIPO_CHOICES,default='R')
    pago = models.CharField(max_length=1,choices=PAGO_CHOICES,default='E')





    
    

