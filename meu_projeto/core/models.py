from django.db import models

class cliente(models.Model):
    codigo = models.IntegerField()
    nome = models.CharField(max_length=100)
    
    def __str__(self):
        return self.codigo,self.nome
    
class vendedor(models.Model):
    codigo = models.IntegerField()
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome
    
class produto(models.Model):
    codigo = models.IntegerField()
    descricao = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10,decimal_places=2)
    quantidadeestoque = models.DecimalField(max_digits=10,decimal_places=2,default=0)