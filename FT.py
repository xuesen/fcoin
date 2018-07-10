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
fcoin.auth(config.key , config.secret)    # 授权

# 写日志
log = Logger('all.log',level='debug')
# 例子
# log.logger.debug('debug')
# log.logger.info('info')
# log.logger.warning('警告')
# log.logger.error('报错')
# log.logger.critical('严重')

#平价买卖
def get_ticket1():
    r = fcoin.get_market_ticker(config.symbol['name'])
    num = (r['data']['ticker'][2] + r['data']['ticker'][4])/2.0
    return pricedecimal(num)#精度控制

#行情 tick 信息, 包含最新成交价, 最新成交量, 买一卖一, 近 24 小时成交量.
def get_ticket2():
    r = fcoin.get_market_ticker(config.symbol['name'])
    #log.logger.info(r)
    return r['data']['ticker']
    # log.logger.info(r['data']['ticker'][2])#最大买一价
    # log.logger.info(r['data']['ticker'][4])#最小卖一价

# 测试买入并返回订单号,tick_price默认价格为实时交易价格，可以自己定价
def testbuy():
    if config.trading_strategy == 1:
        tick_price = get_ticket1()
    else:
        tick_price = get_ticket2()[2]#买一价
    try:
        buy_number = digits(config.mount/tick_price, config.symbol['amount_precision'] )       # 例：btcusdt买btc的数量
        success, buy = fcoin.buy(config.symbol['name'], tick_price, buy_number)

        if success:
            log.logger.info("买入价格：" + str(tick_price) + "买入数量：" + str(buy_number))
            print(buy)
            return buy['data']
        else:
            print(buy)
            return 'FALSE'
    except KeyError:
        pass
# 程序停止时间设置
def sleep(a):
    time.sleep(a)
# 测试卖出并返回订单号,tick_price默认价格为实时交易价格，可以自己定价
def testsell():
    if config.trading_strategy == 1:
        tick_price = get_ticket1()
    else:
        tick_price = get_ticket2()[4]#卖一价
    try:
        sell_number = digits(config.mount/tick_price, config.symbol['amount_precision'] )
        success, sell = fcoin.sell(config.symbol['name'], tick_price, sell_number)

        if success:
            log.logger.info("卖出价格：" + str(tick_price) + "卖出数量：" + str(sell_number))
            print(sell)
            return sell['data']# 返回订单号
        else:
            print(sell)
            return 'FALSE'
    except KeyError:
        pass
# 撤销订单
def order_cancle(order_id):
    log.logger.info("撤销订单")
    r = fcoin.cancel_order(order_id)
# 查询当前订单状态
def orderstate(order_id):
    success, data = fcoin.get_order(order_id)
    if success:
        state = data['data']['state']
        return state
    else:
        return 0

# 循环判断订单完成
def orderjust(order_id):
    flag = 0
    while True:
        try:
            s = orderstate(order_id)
            if s == 'filled':
                log.logger.info("订单已成交")
                return True
            elif s == 'partial_filled':
                log.logger.info(s)
                log.logger.info("+订单部分已成交...")
                sleep(1)
                flag+=1
                if flag == 10:
                    return False
            else:    #刷单流程

                log.logger.info(s)
                log.logger.info("+订单正在等待撮合...")
                sleep(1)
                flag+=1
                if flag == config.order_sleep:
                    return False
        except KeyError:
            pass


# 精度控制，直接抹除多余位数，非四舍五入
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
    return num

# 得到USDT中的余额
def Getusdt():
    try:
        success, data = fcoin.get_balance()
        if success:
            for item in data['data']:
                if item['currency'] == 'usdt':
                    return(float(item['balance']))
        else:
            return 0
    except KeyError:
        pass
# 调试地点
# r = get_ticket()
# log.logger.info(r[2])
# log.logger.info(r[4])

flag = 0#标记
while True:
        # USDT数量是否充足
        try:
            if config.mount > Getusdt():
                log.logger.warning("USDT数量不足")
        except:
            pass
        # 买入
        if flag == 1:
            print("重新卖出")
        else:
            while True:
                order_buyid = testbuy()
                if order_buyid == 'FALSE':
                    log.logger.warning("买入失败")
                    continue
                else:
                    break
            # 循环判断订单完成
            if orderjust(order_buyid) == False:
                log.logger.info("订单等待时间过长，取消订单并重新生成")
                order_cancle(order_buyid)
                flag = 0
                continue

        # 卖出
        while True:
            order_sellid = testsell()
            if order_sellid == 'FALSE':
               log.logger.warning("卖出失败")
               continue
            else:
               break
        # 循环判断订单完成
        if orderjust(order_sellid) == False:
            log.logger.info("订单等待时间过长，取消订单并重新生成")
            order_cancle(order_sellid)
            flag = 1
        else:
            flag = 0

