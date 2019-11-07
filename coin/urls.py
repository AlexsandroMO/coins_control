from django.urls import path
from . import views

urlpatterns = [ 
    path('', views.Cotation, name='url-cotation'),
    path('wallet', views.Wallet, name='url-wallet'),
    path('edit-wallet/<int:id>', views.editWallet, name='url-edit-wallet'),
    path('new_wallet/', views.newWallet, name='url-new-wallet'),
    path('delete_wallet/<int:id>', views.deleteWallet, name='url-delete-wallet'),
    path('pk-wallet/<int:id>', views.pkWallet, name='url-pk-wallet'),
    path('home', views.Home, name='url-home'),
]
