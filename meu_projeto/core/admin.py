from django.contrib import admin
from .models import Cliente
from .models import Vendedor

# Register your models here.
admin.site.register(Cliente)
admin.site.register(Vendedor)

