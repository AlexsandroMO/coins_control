from django.db import models


class TypeWallet(models.Model):
    wallet_type = models.CharField(max_length=20, null=False)

    def __str__(self):
        return str(self.wallet_type)


class MYWallet(models.Model):
    name_wallet = models.CharField(verbose_name='Nome Carteira',max_length=70, null=False)
    var_wallet = models.DecimalField(verbose_name='Valor Inicial da Carteira', max_digits=10, decimal_places=2, default=0)
    type_wallet = models.ForeignKey(TypeWallet, verbose_name='Tipo de Carteira', on_delete=models.CASCADE)
    log_create = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.name_wallet)