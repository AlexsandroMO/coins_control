from django import forms
from .models import MYWallet


class MYWalletForm(forms.ModelForm):
    class Meta:
        model = MYWallet
        fields = ('name_wallet','var_wallet','type_wallet')
