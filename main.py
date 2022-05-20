from xml.etree.ElementInclude import include
import requests
import json
import os
import time


def fetch(type):
    url = "https://livemarketdata-dylanmcdowell37.vercel.app//api/currencies/forex/{type}".format(type=type)

    data = requests.get(url).json()

    res = data['res']
    
    return res

def order(account, units, name, sl, tp):
    headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer 43f645b4da56b5a0b17aba5f6ff1e516-f876bb867a2025add3f62d9a4eb2f60e"
    }
    data = {
        "order": {
            "units": units,
            "instrument": name,        
            "timeInForce": "FOK",
            "type": "MARKET",
            "positionFill": "DEFAULT",
            "stopLossOnFill": {
                "distance": sl
            },
            "takeProfitOnFill": {
                "distance": tp
            }      
        }
    }
    data = json.dumps(data)
    #Practice Account
    r = requests.post(
        'https://api-fxpractice.oanda.com/v3/accounts/{account}/orders'.format(account=account),
        headers=headers,
        data=data
    )
    print(r.text)

def main():
    type = input("Enter type of currency(major or minor): ")
    original = fetch(type)
    print('Running...')
    while True:
        time.sleep(30)
        new = fetch(type)
        for i in range(len(original)):
            if original[i]['rate'] != new[i]['rate']:
                if 'Buy' in new[i]['rate'] and 'Sell' in original[i]['rate'] or 'Sell' in new[i]['rate'] and 'Buy' in original[i]['rate'] or 'Neutral' in original[i]['rate']:
                    if 'Buy' in new[i]['rate']:
                        #post buy to oanda api
                        n = 3
                        name = str(new[i]['name'][:n] + '_' + new[i]['name'][n:]) 
                        sl = round(float(new[i]['price'])*0.001, 3)
                        tp = round(float(new[i]['price'])*0.002, 3)
                        order('101-001-21951911-001', 100, name, str(sl), str(tp))
                        print(name, new[i]['rate'])
                        original = new
                        continue
                    else:
                        #post sell to oanda api
                        n = 3
                        name = str(new[i]['name'][:n] + '_' + new[i]['name'][n:]) 
                        sl = round(float(new[i]['price'])*0.001, 3)
                        tp = round(float(new[i]['price'])*0.002, 3)
                        order('101-001-21951911-005', -100, name, str(sl), str(tp))
                        print(name, new[i]['rate'])
                        original = new
                        continue
                
            else:
                original = new
                continue
            
main()
            
        