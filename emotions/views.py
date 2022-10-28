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
    return render(request, 'create.html')

def index(request):

    r = sr.Recognizer()

    with sr.Microphone() as source:
        # print('당신의 기분은 어떠신가요? : ')
        playsound("output.mp3")
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
    # print(text)
    data = {
        "content": content,
    }
    print(json)
    print(json.dumps(data, indent=4, sort_keys=True))
    response = requests.post(url, data=json.dumps(data), headers=headers)
    rescode = response.status_code

    if(rescode == 200):
        print (response.text)
    else:
        print("Error : " + response.text)
    text = response.json()
    context = {
        'text' : text,
        'data' : data,
    }
    
    return render(request, 'emotions/index.html', context)

def create(request):
    if request.method == 'POST':
        emotion_form = EmotionForm(request.POST)
        if emotion_form.is_valid():
            emotion_form.save()
            return redirect('emotions:index')
    else:
        emotion_form = EmotionForm()
    context = {
        'emotion_form': emotion_form,
    }
    return render(request, 'emotions/create.html', context)