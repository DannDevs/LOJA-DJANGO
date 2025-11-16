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