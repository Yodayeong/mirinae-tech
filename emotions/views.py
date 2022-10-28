from django.shortcuts import render, redirect
from .models import Emotion
from .forms import EmotionForm
import speech_recognition as sr
from playsound import playsound
import sys
import requests
import json

# answer = []

# r = sr.Recognizer()

# with sr.Microphone() as source:
#     # print('당신의 기분은 어떠신가요? : ')
#     playsound("output.mp3")
#     audio = r.listen(source)

#     try:
#         text = r.recognize_google(audio, language="ko-KR")
#         # print('{}'.format(text))
#         answer.append(text)
#     except:
#         print('죄송합니다. 정확히 인식하지 못했습니다.')


def create(request):
    return render(request, 'emotions/create.html')

def index(request):
    return render(request, 'emotions/index.html')
    
def call(request):
    r = sr.Recognizer()

    with sr.Microphone() as source:
        # print('당신의 기분은 어떠신가요? : ')
        playsound("sleep.mp3")
        audio = r.listen(source)

        try:
            text = r.recognize_google(audio, language="ko-KR")
            # print('{}'.format(text))
        except:
            print('죄송합니다. 정확히 인식하지 못했습니다.')

    client_id = "qaxffu4z5i"
    client_secret = "tzh2FdbETgDUPXoUXpy4NRabEnhdQ2c68ZaL0mto"
    url="https://naveropenapi.apigw.ntruss.com/sentiment-analysis/v1/analyze"
    headers = {
        "X-NCP-APIGW-API-KEY-ID": client_id,
        "X-NCP-APIGW-API-KEY": client_secret,
        "Content-Type": "application/json"
    }
    content = text
    data = {
        "content": content,
    }
    # print(json)
    # print(json.dumps(data, indent=4, sort_keys=True))
    response = requests.post(url, data=json.dumps(data), headers=headers)
    rescode = response.status_code

    # if(rescode == 200):
    #     print (response.text)
    # else:
    #     print("Error : " + response.text)
    text = response.json()
    context = {
        'text' : text,
        'data' : data,
    }
    # 터미널 결과창
    # print(text)
    print('사용자가 말한 내용 :', data['content'])
    for line in text['sentences']:
        print('문장 :', line['content'])
        if line['sentiment'] == 'positive':
            print('이 감정은 긍정적으로 판단됩니다.')
        elif line['sentiment'] == 'negative':
            print('이 감정은 부정적으로 판단됩니다.')
        else:
            print('이 감정은 중립적으로 판단됩니다.')
        print('---------------------------------------------------')
    print('전체 문장의 감정상태는', text['document']['sentiment'],'입니다.')   
    return render(request, 'emotions/index.html', context)
