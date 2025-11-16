from django.contrib import admin
from .models import cliente
from .models import vendedor

# Register your models here.
admin.site.register(cliente)
admin.site.register(vendedor)

