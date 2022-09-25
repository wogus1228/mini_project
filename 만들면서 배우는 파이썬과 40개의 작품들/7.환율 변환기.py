# 환율변환 라이브러리를 활용한 환율값 출력
# pip install currencyconverter # 환율 계산을 위한 라이브러리

from currency_converter import CurrencyConverter

cc = CurrencyConverter('http://www.ecb.europa.eu/stats/eurofxref/eurofxref.zip')
print(cc.convert(1, 'USD', 'KRW'))


# 크롤링을 통한 실시간 환율값 출력
from urllib import response

import requests
from bs4 import BeautifulSoup

def get_exchange_rate(target1, target2):
    headers = {
        'User-Agent' : 'Mozilla/5.0',
        'Content-Type' : 'text/html; charset=utf-8'
    }
    
    response = requests.get('https://kr.investing.com/currencies/{}-{}'.format(target1, target2), headers=headers)
    content = BeautifulSoup(response.content, 'html.parser')
    containers = content.find('span', {'data-test': 'instrument-price-last'})
    print(containers.text)
    
get_exchange_rate('usd', 'krw')
