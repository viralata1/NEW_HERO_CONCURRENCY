
import config
import candlestick
import get_position
import binance_futures_api
from datetime import datetime
from termcolor import colored

def lets_make_some_money(i):
    response = binance_futures_api.position_information(i)
    klines_1min  = binance_futures_api.KLINE_INTERVAL_1MINUTE(i)
    klines_3min = binance_futures_api.KLINE_INTERVAL_3MINUTE(i)
    klines_5min = binance_futures_api.KLINE_INTERVAL_5MINUTE(i)
    klines_30min = binance_futures_api.KLINE_INTERVAL_30MINUTE(i)
    position_info = get_position.get_position_info(i, response)
    profit_threshold = get_position.profit_threshold()

    closing_dataset = candlestick.closing_price_list(klines_30min)


    leverage = config.leverage[i]
    if int(response.get("leverage")) != leverage: binance_futures_api.change_leverage(i, leverage)
    if response.get('marginType') != "isolated": binance_futures_api.change_margin_to_ISOLATED(i)

    if position_info == "LONGING":
        if EXIT_LONG(response, profit_threshold, klines_1min): binance_futures_api.close_position(i, "LONG")
        else: print(colored("ACTION           :   HOLDING_LONG", "green"))

    elif position_info == "SHORTING":
        if EXIT_SHORT(response, profit_threshold, klines_1min): binance_futures_api.close_position(i, "SHORT")
        else: print(colored("ACTION           :   HOLDING_SHORT", "red"))

    else:
        if not hot_zone(klines_1min, klines_30min):
            if GO_LONG( klines_1min,  klines_3min, klines_5min, klines_30min): binance_futures_api.open_position(i, "LONG", config.quantity[i])
            elif GO_SHORT( klines_1min, klines_3min, klines_5min, klines_30min): binance_futures_api.open_position(i, "SHORT", config.quantity[i])
            else: print("ACTION           :   🐺 WAIT 🐺")
        else: print("ACTION           :   🐺 WAIT 🐺")

    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

def hot_zone(klines_1min, klines_30min):
    if klines_30min[-1][0] == klines_1min[-1][0]: return True

def GO_LONG(rsi, klines_1min, klines_3min, klines_5min, klines_30min):
    if float(klines_3min[-1][1]) < float(klines_3min[-1][4]) and \
       float(klines_30min[-1][1]) < float(klines_30min[-1][4]):
        return True

def GO_SHORT(rsi, klines_1min, klines_3min, klines_5min, klines_30min):
   if float(klines_3min[-1][1]) < float(klines_3min[-1][4]) and \
       float(klines_30min[-1][1]) < float(klines_30min[-1][4]):
        return True
   
def EXIT_LONG(response, profit_threshold, klines_1MIN):
   if float(klines_1MIN[-1][1]) < float(klines_1MIN[-1][4]) and \
       float(klines_1MIN[-1][1]) < float(klines_1MIN[-1][4]):
        return True
        
def EXIT_SHORT(response, profit_threshold, klines_1MIN):
    if float(klines_1MIN[-1][1]) < float(klines_1MIN[-1][4]) and \
       float(klines_1MIN[-1][1]) < float(klines_1MIN[-1][4]):
        return True