from xml.etree.ElementInclude import include
import requests

symbol = 'EURUSD'
newRec = 'BUY'
data = (symbol + ' ' + newRec)
headers = {}
values = {"text": "@dylan.mcdowell.iarc "+ data}
response = requests.post('https://mattermost.energy.gov/hooks/w4q66gsjcbg67yzw8tw4amhgry', headers=headers, data=values)
