#coding:utf-8
import  configparser
conf = configparser.ConfigParser()
conf.read("conf.ini")

key = conf.get("section", "key")
secret = conf.get("section", "secret")

#精度和最小挂单量
btc = {'name': 'btcusdt', 'coin': 'btc', 'price_precision': 2, 'amount_precision': 4, 'min_amount': 0.001}
eth = {'name': 'ethusdt', 'coin': 'eth', 'price_precision': 2, 'amount_precision': 4, 'min_amount': 0.001}
bch = {'name': 'bchusdt', 'coin': 'bch', 'price_precision': 2, 'amount_precision': 4, 'min_amount': 0.001}
ltc = {'name': 'ltcusdt', 'coin': 'ltc', 'price_precision': 2, 'amount_precision': 4, 'min_amount': 0.001}
etc = {'name': 'etcusdt', 'coin': 'etc', 'price_precision': 2, 'amount_precision': 4, 'min_amount': 0.001}
xrp = {'name': 'xrpusdt', 'coin': 'xrp', 'price_precision': 4, 'amount_precision': 1, 'min_amount': 5}
ft = {'name': 'ftusdt', 'coin': 'ft', 'price_precision': 6, 'amount_precision': 0, 'min_amount': 5}
zip = {'name': 'zipusdt', 'coin': 'zip', 'price_precision': 6, 'amount_precision': 0, 'min_amount': 5}
fi = {'name': 'fiusdt', 'coin': 'fi', 'price_precision': 6, 'amount_precision': 0, 'min_amount': 5}
btm = {'name': 'btmusdt', 'coin': 'btm', 'price_precision': 4, 'amount_precision': 1, 'min_amount': 5}
bnb = {'name': 'bnbusdt', 'coin': 'bnb', 'price_precision': 4, 'amount_precision': 1, 'min_amount': 5}

#FTUSDT，BTCUSDT,ETHUSDT买单数量不少于10usdt


mount  = int(conf.get("section","mount"))         #数量单位USDT
symbol = ""        #交易对
trans = conf.get("section","symbol")
if trans == 'btc':
    symbol = btc
if trans == 'eth':
    symbol = eth
if trans == 'bch':
    symbol = bch
if trans == 'ltc':
    symbol = ltc
if trans == 'etc':
    symbol =etc
if trans == 'xrp':
    symbol = xrp
if trans == 'ft':
    symbol = ft
if trans == 'zip':
    symbol = zip
if trans == 'fi':
    symbol = fi
if trans == 'btm':
    symbol = btm
if trans == 'bnb':
    symbol = bnb

order_sleep = int(conf.get("section","order_sleep"))    #订单处理等待时间s

trading_strategy = int(conf.get("section","trading_Strategy"))


