import socket
import requests
import re

in_addr = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
in_addr.connect(("www.google.co.kr", 443)) # 타 사이트에 접속하여 나의 접속정보 확인
print("내부 IP: ", in_addr.getsockname()[0])

req = requests.get("http://ipconfig.kr") # ip주소확인 사이트에 접속
out_addr = re.search(r'IP Address : (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', req.text)[1] # 사이트 페이지 소스에서 정규식 표현을 사용해 ip주소 부분만을 파싱해서 가져옴
print("외부 IP: ", out_addr)
