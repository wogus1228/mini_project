from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time, datetime
import requests, json

# 사이트 정보
driver_path = # 크롬드라이버 설치 경로 # xattr -d com.apple.quarantine chromedriver (드라이브 파일 권한 설정 필요)
homepage_url = "https://etk.srail.kr/cmc/01/selectLoginForm.do?pageId=TK0701000000" # 접속할 사이트 주소

# 접속정보
member_number = # 회원번호
password = # 비밀번호

# 예약정보
departure = "동탄" # 출발지
destination = "광주송정" # 도착지
reservation_date = "20220505" # 예약일
reservation_time = "080000" # 예약시간


def connect():
    # 크롬 드라이버 사용을 위한 로딩
    driver = webdriver.Chrome(executable_path=driver_path)

    return driver


def login(driver, member_number, password):
    # 크롬 드라이버를 이용한 SRT 로그인 페이지 로드
    driver.get(homepage_url)

    # 회원번호 입력
    driver.find_element(By.ID, 'srchDvNm01').send_keys(member_number)

    # 비밀번호 입력
    driver.find_element(By.ID, 'hmpgPwdCphd01').send_keys(password)

    # 확인 버튼 클릭
    driver.find_element(By.XPATH,
                        '/html/body/div/div[4]/div/div[2]/form/fieldset/div[1]/div[1]/div[2]/div/div[2]/input').click()

    print("로그인에 성공했습니다.")

    return driver


def send_kakao_msg(msg):
    # 카카오톡 전송을 위한 토큰 로딩
    with open("kakao_code.json", "r") as fp:
        tokens = json.load(fp)

    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"

    headers = {
        "Authorization": "Bearer " + tokens["access_token"]
    }

    # 메시지 생성
    data = {
        "template_object": json.dumps({
            "object_type": "text",
            "text": msg,
            "link": {
                "web_url": "www.naver.com"
            }
        })
    }

    # 카카오톡 메시지 전송
    response = requests.post(url, headers=headers, data=data)
    response.status_code


def reserve(driver):
    # 개발변수
    reserved = False  # 예약여부
    reload_number = 1  # 새로고침 카운트

    # 기차 예매 페이지로 이동
    driver.get('https://etk.srail.kr/hpg/hra/01/selectScheduleList.do?pageId=TK0101010000')

    # 로딩 시간을 위해 3초 기다림
    driver.implicitly_wait(3)

    # 열려있는 창 정보 불러오기
    #windows = driver.window_handles

    # 메인 창을 제외한 다른 창 닫기
    #driver.switch_to.window(windows[1])
    #driver.close()

    # 메인 창으로 돌아오기
    #driver.switch_to.window(windows[0])

    # 출발지 입력
    dptRsStn = driver.find_element(By.ID, 'dptRsStnCdNm')
    dptRsStn.clear()
    dptRsStn.send_keys(departure)

    # 도착지 입력
    arvRsStn = driver.find_element(By.ID, 'arvRsStnCdNm')
    arvRsStn.clear()
    arvRsStn.send_keys(destination)

    # 출발일자 입력
    Select(driver.find_element(By.ID, 'dptDt')).select_by_value(reservation_date)

    # 출발시간 입력
    Select(driver.find_element(By.ID, 'dptTm')).select_by_value(reservation_time)

    # 조회하기 버튼 클릭
    driver.find_element(By.XPATH, '/html/body/div/div[4]/div/div[2]/form/fieldset/div[2]/input').click()
    # 로딩 시간을 위해 5초 기다림
    driver.implicitly_wait(5)

    print("출발지 : [" + departure + "] ---> " + "도착지 : [" + destination + "]")
    result_date = datetime.datetime.strptime(reservation_date, '%Y%m%d')
    print(str(result_date)[0:10] + "일자의 " + reservation_time[0:2] + "시 이후 내역을 조회합니다..")

    # 기차내역 리스트
    train_list = driver.find_elements(By.CSS_SELECTOR, '#result-form > fieldset > div.tbl_wrap.th_thead '
                                                       '> table > tbody > tr')

    print("[열차 리스트]")
    # 기차내역 리스트 출력
    for i in range(1, 3): #len(train_list)+1):
        for j in range(3, 6):
            text = driver.find_element(By.CSS_SELECTOR,
                                       f"#result-form > fieldset > div.tbl_wrap.th_thead > table > tbody > tr:nth-child({i}) > td:nth-child({j})").text.replace("\n"," ")
            print(text, end=" ")
        print()

    # 전체 리스트 중 예약가능한 리스트가 있는지 반복적으로 검색
    while True:
        for i in range(1, 3): #len(train_list)+1):
            available_reserve = driver.find_element(By.CSS_SELECTOR,
                                                    f"#result-form > fieldset > div.tbl_wrap.th_thead > table > tbody > tr:nth-child({i}) > td:nth-child(7)").text

            # 예약하기가 가능한 경우
            if "예약하기" in available_reserve:
                print("예약성공!")
                # 예약하기 버튼 클릭
                driver.find_element(By.CSS_SELECTOR,
                                    f"#result-form > fieldset > div.tbl_wrap.th_thead > table > tbody > tr:nth-child({i}) > td:nth-child(7) > a").click()
                # 메시지 생성
                msg = "[예약정보안내]\n" + "열차번호 : [" + driver.find_element(By.CSS_SELECTOR, f"#result-form > fieldset > div.tbl_wrap.th_thead > table > tbody > tr:nth-child({i}) > td:nth-child({3})").text.replace("\n", " ") + "]\n" + "출발정보 : [" + driver.find_element(By.CSS_SELECTOR, f"#result-form > fieldset > div.tbl_wrap.th_thead > table > tbody > tr:nth-child({i}) > td:nth-child({4})").text.replace("\n", " ") + "]\n" + "도착정보 : [" + driver.find_element(By.CSS_SELECTOR, f"#result-form > fieldset > div.tbl_wrap.th_thead > table > tbody > tr:nth-child({i}) > td:nth-child({5})").text.replace("\n", " ") + "]\n" + "앱에 접속하여 10분 내에 결제를 완료하세요."

                # 카카오 메시지 전송
                #send_kakao_msg(msg)
                # 3초 지연
                driver.implicitly_wait(3)
                # 예약 완료 처리
                reserved = True
                break

            elif "신청하기" in available_reserve:
                print("예약대기성공!")
                # 예약대기 버튼 클릭
                driver.find_element(By.CSS_SELECTOR,
                                    f"#result-form > fieldset > div.tbl_wrap.th_thead > table > tbody > tr:nth-child({i}) > td:nth-child(8) > a").click()

                # 3초 지연
                driver.implicitly_wait(3)

                # 예약 완료 처리
                reserved = True
                break

        # 예약이 안된 경우
        if not reserved:
            # 5초 기다림
            time.sleep(3)

            # 재조회
            submit = driver.find_element(By.XPATH, "/html/body/div/div[4]/div/div[2]/form/fieldset/div[2]/input")
            driver.execute_script("arguments[0].click();", submit)
            print("전차량 매진으로 새로고침 시도합니다. 새로고침 횟수 : [" + str(reload_number) + "]")
            reload_number += 1

            driver.implicitly_wait(10)
            time.sleep(3)

        # 예약에 성공한 경우
        else:
            break


if __name__ == "__main__":
    driver = connect()
    driver = login(driver, member_number, password)
    reserve(driver)
