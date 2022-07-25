import random

random_number = random.randint(1, 100) # 1~100 사이의 랜덤 숫자 생성

game_count = 1 # 반복입력 횟수 체크

while True:
    try:
        my_number = int(input("1~100 사이의 숫자를 입력하세요:"))
        
        if my_number > random_number:
            print("Down")
        elif my_number < random_number:
            print("Up")
        elif my_number == random_number:
            print(f"축하합니다.{game_count}회 만에 맞췄습니다.")
            break
        
        game_count += 1
    except: # 문자 입력 시, 재입력
        print("숫자를 입력하세요.") 
