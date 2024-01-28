from django.contrib import admin
from .models import Client,Admin,Avocat,User
# Register your models here.

admin.site.register(User)
admin.site.register(Admin)
admin.site.register(Avocat)
admin.site.register(Client)

