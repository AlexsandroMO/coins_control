import pandas as pd
import lxml
import json
import requests
# import re
from datetime import date
from datetime import datetime
from datetime import date, datetime
import time
import Read_SQL
import Write_SQL
import os

def joi_name(name_wallet):
    join_name = name_wallet.split()

    if len(join_name) == 1:
        name_wallet = '{}'.format(join_name[0])
        return name_wallet
        #print('\n\n\n>>>>>>>>>>>>: ',name_wallet)

    elif len(join_name) == 2:
        name_wallet = '{}_{}'.format(join_name[0], join_name[1])
        return name_wallet
        #print('\n\n\n>>>>>>>>>>>>: ',name_wallet)

    elif len(join_name) == 3:
        name_wallet = '{}_{}_{}'.format(join_name[0], join_name[1], join_name[2])
        return name_wallet
        #print('\n\n\n>>>>>>>>>>>>: ',name_wallet)

def take_take(take1, take2):
    takeA = take1[3][7:len(take1[3]) -1:]
    takeB = take1[4][:len(take1[4]) -1:]
    takeC = take1[5][:len(take1[5]) -1:]
    takeD = take2[3][7:len(take2[3]) -1:]

    list_take = [takeA,takeB,takeC,takeD]
    
    if list_take[2] == 'require':
        df = [list_take[0], list_take[3]]
        return df

    take_all =[]
    for a in list_take:
        if len(a) < 13:
            take_all.append(a)
        else:
            if a != 'maxlength="70':
                take_all.append(a)

    new = []
    for a in range(len(take_all) -1):
        new.append(take_all[a])

    if len(new) == 2:
        name = '{}_{}'.format(new[0], new[1])
        df = [name, list_take[3]]
        return df

    elif len(new) == 3:
        name = '{}_{}_{}'.format(new[0], new[1], new[2])
        df = [name, list_take[3]]
        return df


def win_lose_controll(win_lose, last_BTC_buy):
    win_lose = 0,00
    BTC = bitcoin()
    if BTC[1] != last_BTC_buy[-1]:
        win_lose = (BTC[1] - last_BTC_buy[-1])
        return float(win_lose)
    else:
        return 0.00


def bitcoin():
    #Sistema de Cotação
    current_date = datetime.now()
    now_date = current_date.strftime('%d/%m/%Y %H:%M:%S')

    list_btc = requests.get('https://api.bitcointrade.com.br/v2/public/BRLBTC/ticker')
    btc_cotation = json.loads(list_btc.text)
    btc_last = btc_cotation['data']['last'] # Ultimo Biticoin negociado
    btc_buy = btc_cotation['data']['buy'] # Ultimo Biticoin negociado
    btc_sell = btc_cotation['data']['sell'] # Ultimo Biticoin negociado

    list_BTC = [btc_last, btc_buy, btc_sell, now_date]

    return list_BTC
    
def other_coins():
    #Sistema de Cotação
    list_coins = requests.get('https://economia.awesomeapi.com.br/all')

    cotation_coins = json.loads(list_coins.text)
    usd_buy = cotation_coins['USD']['high']
    usd_sell = cotation_coins['USD']['low']
    eur_buy = cotation_coins['EUR']['high']
    eur_sell = cotation_coins['EUR']['low']
    peso_buy = cotation_coins['ARS']['high']
    peso_sell = cotation_coins['ARS']['low']
    iene_buy = cotation_coins['JPY']['high']
    iene_sell = cotation_coins['JPY']['low']

    cotation_all = [usd_buy, usd_sell, eur_buy, eur_sell, peso_buy, peso_sell, iene_buy, iene_sell]

    return cotation_all


def Wallet_pen():
    cotation = bitcoin()

    Write_SQL.add_var_bitcoin(cotation[0], cotation[1], cotation[2], cotation[3])
    Write_SQL.add_var_wallet(50000, 0.00, cotation[3])


def start_cotation(var_wallet, name_wallet):
    cotation = bitcoin()

    wallet = float(var_wallet)
    btc_x_wallet = wallet / float(cotation[1]) #Valor em Bitcoin da carteira
    win_lose = 0.00 #Ganhos e perdas da transação

    BTC_last_buy = Read_SQL.read_sql_btc()

    last_BTC_buy = []
    for i in BTC_last_buy['VAR_BTC_BUY']:
        last_BTC_buy.append(i)

    last_datas = Read_SQL.read_sql_wallet(name_wallet)

    last_wallet = []
    for i in last_datas['VAR_WALLET']:
        last_wallet.append(i)

    lose_win = win_lose_controll(win_lose, last_BTC_buy)

    if lose_win != 0.00:
        result_wallet = last_wallet[-1] + lose_win
        #Write_SQL.add_var_wallet(result_wallet,lose_win,cotation[3])
        Write_SQL.add_var_wallet_start(result_wallet,lose_win,cotation[3],name_wallet)

    Write_SQL.add_var_bitcoin(cotation[0], cotation[1], cotation[2], cotation[3])

    print('\n')
    print('|========= CONTROLE DE MOEDAS =============|')
    print('|******************************************|')
    print('|Valor de Compra:            {}'.format(cotation[1]))
    print('|Venda:                      {}'.format(lose_win))
    print('|valor da carteira em BTC:   {}'.format(round(btc_x_wallet,2))) 
    print('|Carteira:                   {}'.format(last_wallet[-1]))
    print('|******************************************|\n')

    print('|=====================> HISTÓRICO DE AÇÕES <========================|')
    print('|Ultima Transações                                                  |\n') 
    print(BTC_last_buy.tail(2))
    print('\n|Carteira                                                         |\n') 
    print(last_datas.head(2))

    list_my_cotations = [cotation[1], round(lose_win,2), round(btc_x_wallet,2), round(last_wallet[-1],2)]
    
    return list_my_cotations
