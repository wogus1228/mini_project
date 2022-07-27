# pip install gtts 
# gtts : 문자를 음성으로 변환해주는 라이브러리

# pip install playsound
# playsound : mp3 파일을 파이썬에서 재생하기 위한 라이브러리

from gtts import gTTS
from playsound import playsound
import os

# 현재 경로를 기본 경로로 설정
os.chdir(os.path.dirname(os.path.abspath(__file__)))

file_path = '3_sample.txt'
with open(file_path, 'rt', encoding='UTF8') as f:
    read_file = f.read()

tts = gTTS(text=read_file, lang='ko')

tts.save("myText.mp3")

playsound("myText.mp3")
