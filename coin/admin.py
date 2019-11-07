
from django.contrib import admin
from .models import TypeWallet, MYWallet


class ListaMYWallet(admin.ModelAdmin):
    list_display = ('name_wallet','var_wallet','type_wallet','log_create')

admin.site.register(TypeWallet)
admin.site.register(MYWallet, ListaMYWallet)
