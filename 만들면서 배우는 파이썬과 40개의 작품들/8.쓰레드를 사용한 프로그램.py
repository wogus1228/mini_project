import threading
import time

def sum(name, value):
    for i in range(0, value):
        print(f'{name} : {i}')

t1 = threading.Thread(target=sum, args=('1번 쓰레드', 10))
t2 = threading.Thread(target=sum, args=('2번 쓰레드', 10))

t1.start()
t2.start()

print('Main Thread')

def thread_1():
    while True:
        print('쓰레드1 동작')
        time.sleep(1.0)
        
t1 = threading.Thread(target=thread_1)
t1.daemon = True # 메인 쓰레드를 데몬쓰레드로 설정하여 메인동작이 실행될 때만 쓰레드를 실행하도록 함
t1.start()

while True:
    print('메인동작')
    time.sleep(2.0)
