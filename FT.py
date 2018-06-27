#coding:utf-8
from fcoin3 import Fcoin
from Logging import Logger
import time
import json
import sys
import traceback
import math
import config

fcoin = Fcoin()
fcoin.auth(config.key , config.secret)    


log = Logger('all.log',level='debug')




def get_trades():
    r=fcoin.get_trades(config.symbol['name'])
    return r['data'][0]['price']
def testbuy(tick_price = get_trades()):
    try:
        buy_number = round(config.mount/tick_price,2)     
        success, buy = fcoin.buy(config.symbol['name'], get_trades(), buy_number)

        log.logger.info("买入价格：" + str(tick_price) +"买入数量：" + str(buy_number))
        if success:
            print(buy)
            return buy['data']
        else:
            print(buy)
            return 'FALSE'
    except KeyError:
        pass

def sleep(a):
    time.sleep(a)
def testsell(tick_price = get_trades()):
    try:
        sell_number = round(config.mount/tick_price, 2)
        success, sell = fcoin.sell(config.symbol['name'], tick_price, sell_number)

        log.logger.info("卖出价格：" + str(tick_price) +"卖出数量：" + str(sell_number))
        if success:
            print(sell)
            return sell['data']
        else:
            print(sell)
            return 'FALSE'
    except KeyError:
        pass
def order_cancle(order_id):
    log.logger.info("撤销订单")
    r = fcoin.cancel_order(order_id)
def orderstate(order_id):
    success, data = fcoin.get_order(order_id)
    if success:
        state = data['data']['state']
        return state

def orderjust(order_id):
    flag = 0
    while True:
        try:
            s = orderstate(order_id)
            if s == 'filled':
                return True
            else:
                log.logger.info(s)
                log.logger.info("+订单正在等待撮合...")
                flag+=1
                if flag == config.order_sleep:
                    return False
        except KeyError:
            pass


def digits(num, digit):
    site = pow(10, digit)
    tmp = num * site
    tmp = math.floor(tmp) / site
    return tmp
def pricedecimal(num):
    if config.symbol['name'] == 'ftusdt':
        num = digits(num, 6)
    elif config.symbol['name'] == 'btmusdt':
        num = digits(num, 4)
    else:
        num = digits(num, 2)

def Getusdt():
    success, data = fcoin.get_balance()
    if success:
        for item in data['data']:
            if item['currency'] == 'usdt':
                return(float(item['balance']))

log.logger.info('USDT余额:%s' % Getusdt())
log.logger.info('使用交易对:'+str(config.symbol['name']))
log.logger.info('交易对象市价'+str(get_trades()))

while True:
        if config.mount > Getusdt():
            log.logger.warning("USDT数量不足")
        else:
            while True:
                order_id = testbuy()
                if order_id == 'FALSE':
                    log.logger.warning("买入失败")
                    continue
                else:
                    break
            if orderjust(order_id) == False:
                log.logger.info("订单等待时间过长，取消订单并重新生成")
                order_cancle(order_id)
                continue

            while True:
                order_id = testsell()
                if order_id == 'FALSE':
                    log.logger.warning("卖出失败")
                    continue
                else:
                    break
            if orderjust(order_id) == False:
                log.logger.info("订单等待时间过长，取消订单并重新生成")
                order_cancle(order_id)
                continue


