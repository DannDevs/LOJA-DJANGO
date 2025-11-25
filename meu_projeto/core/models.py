from django.db import models

class cliente(models.Model):
    codigo = models.IntegerField()
    nome = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.codigo} - {self.nome}"
    
class vendedor(models.Model):
    codigo = models.IntegerField()
    nome = models.CharField(max_length=100)

    def __str__(self):
        return f" {self.codigo} - {self.nome}"
    
class produto(models.Model):
    codigo = models.IntegerField()
    descricao = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10,decimal_places=2)
    quantidadeestoque = models.DecimalField(max_digits=10,decimal_places=2,default=0)

    def __str__(self):
        return f"{self.codigo} - {self.descricao}"

class venda(models.Model):
    codigo = models.IntegerField()
    cliente = models.ForeignKey(cliente, on_delete=models.PROTECT)
    vendedor = models.ForeignKey(vendedor, on_delete=models.PROTECT)
    valor = models.DecimalField(max_digits=10,decimal_places=2)

class itemvenda(models.Model):
    venda = models.ForeignKey(venda, on_delete=models.CASCADE)
    produto = models.ForeignKey(produto, on_delete=models.PROTECT)
    quantidade = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    preco_unitario = models.DecimalField(max_digits=10,decimal_places=2,default=0)

    def __init__(self):
        return f"{self.produto}"

class movimentoitem(models.Model):
    codigo = models.IntegerField()
    tipomovimento = models.CharField() 
    produto = models.ForeignKey(produto,on_delete=models.CASCADE)
    qtdmovimento = models.DecimalField(max_digits=8,decimal_places=2,default=0)

    
    

