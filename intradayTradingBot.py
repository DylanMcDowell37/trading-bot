from xml.etree.ElementInclude import include
import requests
import numpy as np
import MetaTrader5 as mt5
import time
from tradingview_ta import TA_Handler, Interval, Exchange


inputArray = [
    {
        "symbol": "EURUSD",
        "screener": "forex",
        "exchange": Exchange.FOREX,
        "open": 7,
        "close": 19,
        "tp": 500,
        "sl": 250,
    },
    {
        "symbol": "USDJPY",
        "screener": "forex",
        "exchange": Exchange.FOREX,
        "open": 12,
        "close": 8,
        "tp": 400,
        "sl": 250,
    },
    {
        "symbol": "NZDUSD",
        "screener": "forex",
        "exchange": Exchange.FOREX,
        "open": 12,
        "close": 8,
        "tp": 500,
        "sl": 250,
    },
    {
        "symbol": "USDCHF",
        "screener": "forex",
        "exchange": Exchange.FOREX,
        "open": 7,
        "close": 19,
        "tp": 500,
        "sl": 250,
    },
    {
        "symbol": "USDCAD",
        "screener": "forex",
        "exchange": Exchange.FOREX,
        "open": 12,
        "close": 21,
        "tp": 500,
        "sl": 250,
    },
    {
        "symbol": "AUDUSD",
        "screener": "forex",
        "exchange": Exchange.FOREX,
        "open": 12,
        "close": 8,
        "tp": 500,
        "sl": 250,
    },
    {
        "symbol": "GBPUSD",
        "screener": "forex",
        "exchange": Exchange.FOREX,
        "open": 7,
        "close": 19,
        "tp": 500,
        "sl": 250,
    },

]



def fetch():
    handler = TA_Handler
    outputArray = []
    for i in range(len(inputArray)):
        data = handler(
            symbol= inputArray[i]['symbol'],
            exchange= inputArray[i]['exchange'],
            screener= inputArray[i]['screener'],
            interval= Interval.INTERVAL_5_MINUTES,
            timeout=None
        )
        outputArray.append(data.get_analysis().moving_averages)
    return outputArray

def fetchComp():
    handler = TA_Handler
    outputArray = []
    for i in range(len(inputArray)):
        data = handler(
            symbol= inputArray[i]['symbol'],
            exchange= inputArray[i]['exchange'],
            screener= inputArray[i]['screener'],
            interval= Interval.INTERVAL_1_HOUR,
            timeout=None
        )
        outputArray.append(data.get_analysis().moving_averages)
    return outputArray

def fetchComptwo():
    handler = TA_Handler
    outputArray = []
    for i in range(len(inputArray)):
        data = handler(
            symbol= inputArray[i]['symbol'],
            exchange= inputArray[i]['exchange'],
            screener= inputArray[i]['screener'],
            interval= Interval.INTERVAL_1_DAY,
            timeout=None
        )
        outputArray.append(data.get_analysis().moving_averages)
    return outputArray

def mtbuyrequest(symbol, sl, tp, lot):
    symbol_info = mt5.symbol_info(symbol + '.HKT')
    if symbol_info is None:
        print(symbol + '.HKT', "not found, can not call order_check()")
        return
    if not symbol_info.visible:
        print(symbol + '.HKT', "is not visible, trying to switch on")
        return
    point = mt5.symbol_info(symbol + '.HKT').point
    price = mt5.symbol_info_tick(symbol + '.HKT').ask    
    
    deviation = 20
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol + '.HKT',
        "volume": lot,
        "type": mt5.ORDER_TYPE_BUY,
        "price": price,
        "sl": round(price - sl * point, 5),
        "tp": round(price + tp * point, 5),
        "deviation": deviation,
        "magic": 234000,
        "comment": "python script open",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_FOK,
    }
    result = mt5.order_send(request)
    print("1. order_send(): by {} {} lots at {} with deviation={} points".format((symbol + '.HKT'),lot,price,deviation))
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("2. order_send failed, retcode={}".format(result.retcode))
    # request the result as a dictionary and display it element by element
    result_dict=result._asdict()
    for field in result_dict.keys():
        print("   {}={}".format(field,result_dict[field]))
        # if this is a trading request structure, display it element by element as well
        if field=="request":
            traderequest_dict=result_dict[field]._asdict()
            for tradereq_filed in traderequest_dict:
                print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
    print("2. order_send done, ", result)
    print("   opened position with POSITION_TICKET={}".format(result.order))
    print("   sleep 2 seconds before closing position #{}".format(result.order))
    time.sleep(2)
    
def mtsellrequest(symbol, sl, tp, lot):
    symbol_info = mt5.symbol_info(symbol + '.HKT')
    if symbol_info is None:
        print(symbol + '.HKT', "not found, can not call order_check()")
        return
    if not symbol_info.visible:
        print(symbol + '.HKT', "is not visible, trying to switch on")
        return
    point = mt5.symbol_info(symbol + '.HKT').point
    price = mt5.symbol_info_tick(symbol + '.HKT').bid
    
    deviation = 20
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol + '.HKT',
        "volume": lot,
        "type": mt5.ORDER_TYPE_SELL,
        "price": price,
        "sl": round(price + sl * point, 5),
        "tp": round(price - tp * point, 5),
        "magic": 234000,
        "deviation": deviation,
        "comment": "python script open",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_FOK,
    }
    result = mt5.order_send(request)
    print("1. order_send(): by {} {} lots at {} with deviation={} points".format((symbol + '.HKT'),lot,price,deviation))
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("2. order_send failed, retcode={}".format(result.retcode))
    # request the result as a dictionary and display it element by element
    result_dict=result._asdict()
    for field in result_dict.keys():
        print("   {}={}".format(field,result_dict[field]))
        # if this is a trading request structure, display it element by element as well
        if field=="request":
            traderequest_dict=result_dict[field]._asdict()
            for tradereq_filed in traderequest_dict:
                print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
    print("2. order_send done, ", result)
    print("   opened position with POSITION_TICKET={}".format(result.order))
    print("   sleep 2 seconds before closing position #{}".format(result.order))
    time.sleep(2)

def main():
    print("MetaTrader5 package author: ", mt5.__author__)
    print("MetaTrader5 package version: ", mt5.__version__)
 
# establish connection to the MetaTrader 5 terminal
    if not mt5.initialize():
        print("initialize() failed, error code =",mt5.last_error())
        quit()
    # type = input("Enter type of currency(major or minor): ")
    lot = float(input('Please enter your lot size with decimal(EX: 1.0 instead of 1): '))
    original = fetch()
    print('Running...')
    # print(original)
    while True:
        gmt = time.gmtime().tm_hour
        day = time.gmtime().tm_wday
        new = fetch()
        comp = fetchComp()
        compTwo = fetchComptwo()
        # print(new)
        if gmt >=0 and gmt <= 23:
            
            for i in range(len(original)):
                newRec = new[i]['COMPUTE']['Ichimoku'].replace('STRONG_', '')
                originalRec = original[i]['COMPUTE']['Ichimoku'].replace('STRONG_', '')
                compRec = comp[i]['RECOMMENDATION'].replace('STRONG_', '')
                compRectwo = compTwo[i]['RECOMMENDATION'].replace('STRONG_', '')
                open = inputArray[i]["open"]
                close = inputArray[i]["close"]
                tp = inputArray[i]["tp"]
                sl = inputArray[i]["sl"]
                if gmt >= open and gmt <= close:
                    if originalRec != newRec:
                        if 'BUY' in compRec and 'BUY' in compRectwo:
                            if ('SELL' in originalRec or 'NEUTRAL' in originalRec) and 'BUY' in newRec:
                                symbol = inputArray[i]['symbol']
                                symbol_info = mt5.symbol_info(symbol + '.HKT') 
                                if symbol_info is None:
                                    print(symbol + '.HKT', "not found, can not call order_check()")
                                    continue
                                if not symbol_info.visible:
                                    print(symbol + '.HKT', "is not visible, trying to switch on")
                                    continue                       
                                price = mt5.symbol_info_tick(symbol + '.HKT').ask
                                # print(symbol, new[i]['COMPUTE']['Ichimoku'], price)
                                mtbuyrequest(symbol, sl, tp, lot)
                                original = new
                                continue
                            else:
                                continue
                        elif 'SELL' in compRec and 'SELL' in compRectwo:
                            if ('BUY' in originalRec or 'NEUTRAL' in originalRec) and 'SELL' in newRec:
                                symbol = inputArray[i]['symbol']
                                symbol_info = mt5.symbol_info(symbol + '.HKT')
                                if symbol_info is None:
                                    print(symbol + '.HKT', "not found, can not call order_check()")
                                    continue
                                if not symbol_info.visible:
                                    print(symbol + '.HKT', "is not visible, trying to switch on")
                                    continue                        
                                price = mt5.symbol_info_tick(symbol + '.HKT').bid
                                # print(symbol, new[i]['COMPUTE']['Ichimoku'], price)
                                mtsellrequest(symbol, sl, tp, lot)
                                original = new
                                continue
                            else:
                                continue 
                        else:
                            continue 
                    else:
                        continue
                else:
                    continue
        else:
            
            continue
        original = new 
        time.sleep(90)   
main()
            
        