
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import MYWallet
from .forms import MYWalletForm
from django.contrib import messages

import main
import CreateTable_SQL
import Write_SQL


def Home(request):
    return HttpResponse('<h1>Hello!</h1>')


def Cotation(request):
    bitcoin = main.bitcoin()
    all_cotation = main.other_coins()

    return render(request, 'coin/site-cotation.html',{'bitcoin': bitcoin,'all_cotation': all_cotation})


def Wallet(request):
    wallets = MYWallet.objects.all()
    bitcoin = main.bitcoin()
    all_cotation = main.other_coins()

    return render(request, 'coin/lista-carteira.html', {'wallets': wallets, 'bitcoin': bitcoin, 'all_cotation': all_cotation})


def editWallet(request, id):
    wallets = get_object_or_404(MYWallet, pk=id)
    form = MYWalletForm(instance=wallets)

    if request.method == 'POST':
        form = MYWalletForm(request.POST, instance=wallets)

        if form.is_valid():
            wallets.save()
            return redirect('url-wallet')
        else:
            return render(request, 'coin/edit-wallet.html', {'form': form, 'wallets': wallets})

    else:
        return render(request, 'coin/edit-wallet.html', {'form': form, 'wallets': wallets})


def newWallet(request):
    if request.method == 'POST':
        form = MYWalletForm(request.POST)

        txt1 = str(form['name_wallet'])
        txt2 = str(form['var_wallet'])

        take1 = txt1.split()
        take2 = txt2.split()

        name_wallet = main.take_take(take1, take2)

        bitcoin = main.bitcoin()

        if form.is_valid():
            wallets = form.save(commit=False)
            wallets.save()

            CreateTable_SQL.create_Wallet(name_wallet[0])
            Write_SQL.add_var_wallet_start(float(name_wallet[1]), 0.00, bitcoin[3], name_wallet[0])

            return redirect('url-wallet')

    else:
        form = MYWalletForm()
        return render(request, 'coin/add-wallet.html', {'form': form})


def deleteWallet(request, id):
    wallets = get_object_or_404(MYWallet, pk=id)
    wallets.delete()

    messages.info(request, 'Carteira deletada com sucesso.')
    return redirect('url-wallet')


def pkWallet(request, id):
    wallets = get_object_or_404(MYWallet, pk=id)

    bitcoin = main.bitcoin()

    name_wallet = wallets.name_wallet
    name_wallet = main.joi_name(name_wallet)

    start_project = main.start_cotation(wallets.var_wallet, name_wallet)

    print(start_project)


    return render(request, 'coin/my-wallet.html', {'wallets': wallets, 'bitcoin': bitcoin, 'start_project': start_project})


