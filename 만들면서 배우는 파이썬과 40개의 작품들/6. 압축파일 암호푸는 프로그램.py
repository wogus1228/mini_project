# zip -er 압축파일명 압축할 파일명
# -e : encrypt. 압축시 암호 설정
# -r : 압축대상이 폴더일 경우 하위 폴더, 파일 모두 압축

import zipfile
import itertools

def un_zip(passwd_string, min_len, max_len, zFile):
    for len in range(min_len, max_len+1):
        to_attempt = itertools.product(passwd_string, repeat= len)
        for attempt in to_attempt:
            passwd = ''.join(attempt)
            print(passwd)
            try:
                zFile.extractall(pwd = passwd.encode())
                print(f'비밀번호는 {passwd} 입니다.')
                return 1
            except:
                pass

passwd_string = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ' # 패스워드에 들어갈 문자 유형

zFile = zipfile.ZipFile(r'/Users/hyun/Documents/PythonProgramming/파이썬과 40개의 작품들/6.압축파일 암호푸는 프로그램/암호1234.zip') # 암호화된 압축파일 경로

min_len = 1 # 패스워드 최소글자 수
max_len = 5 # 패스워드 최대글자 수

unzip_result = un_zip(passwd_string, min_len, max_len, zFile)
if unzip_result == 1:
    print('암호찾기에 성공하였습니다.')
else:
    print('암호찾기에 실패하였습니다.') 
