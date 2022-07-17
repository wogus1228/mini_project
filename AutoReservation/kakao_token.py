import requests
import json

# 토큰 발급 url
# https://kauth.kakao.com/oauth/authorize?response_type=code&client_id=&redirect_uri=

# 카카오api 관련
url = 'https://kauth.kakao.com/oauth/token'
rest_api_key = # 발급받은 api 키 값
redirect_uri = 'https://www.naver.com'
authorize_code = # 키 값을 사용하여 발급받은 토큰 코드

data = {
    'grant_type':'authorization_code',
    'client_id':rest_api_key,
    'redirect_uri':redirect_uri,
    'code': authorize_code,
}

response = requests.post(url, data=data)
tokens = response.json()
print(tokens)

# json 저장
with open("kakao_code.json", "w") as fp:
    json.dump(tokens, fp)
