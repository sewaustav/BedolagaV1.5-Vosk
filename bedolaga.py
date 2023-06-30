import os
import subprocess
import webbrowser

import vosk
import sys
import sounddevice as sd
import queue

import cv2
import numpy as np
import pyautogui
import time
from random import *
import json

import eel

import openai

import string

import config

import pyttsx3


engine = pyttsx3.init()
engine.setProperty('rate',200)
engine.setProperty('volume',0.9)
voice = engine.getProperty('voice')
engine.setProperty(voice, "!v/m1")


from pyowm import OWM
from pyowm.utils import config as cn
from pyowm.utils import timestamps

openai.api_key = config.TOKEN

model_engine = "text-davinci-003"


model = vosk.Model("smallmodel")


gpt_request = False
gpt_code = False
google_request = False

dialog = False
is_active_command = False

weather = False


samlerate = 16000
device = 1

dialogue_history = ["Ты программист на питоне, который ненавидит с++, тебе 27 лет, твое имя Бедолага, любишь играть в футбол, в шахматы, болеешь за футбольный клуб Тоттенхем, также можешь весь день играть в компьютерные игры, любимая игра  райз оф кингдомс. У тебя много денег, живешь в Греции, летом приезжаешь отдыхать в Калининград. Никогда не говоришьо религии, политики. Можешь внезапно посре дидиалога рассказать шутку. Отвечаешьна вопросы коротко, только по делу, максимум 2 предложения.", "Будет сделано."]

q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)

    q.put(bytes(indata))

def is_valid_line(line):
    if len(line.strip()) == 0:
        return False
    first_char = line.strip()[0]
    if first_char in string.ascii_letters or first_char == "#" or first_char == "{" or first_char == "}" or first_char == "]" or first_char == "[" or first_char == "'" or first_char == '"':
        return True
    return False

def dialog_gpt(message):
    dialogue_history.append(message + ".")
    try:
        response = openai.Completion.create(
            engine=model_engine,
            prompt="\n".join(dialogue_history),
            max_tokens=200,
            temperature=0.5,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
    except openai.OpenAIError as exx:
        if exx.code == "context_length_exceeded":
            # message_log = [system_message, message_log[-1]]
            pass

    reply = response.choices[0].text.strip()
    dialogue_history.append(reply)
    return reply

def weather_func(temp, rain):
    if temp >= 15 and temp < 20 and rain == {}:
        return 'В твоём городе сейчас достаточно тепло, но лучше надеть штаны и кофту'
    elif temp >= 15 and temp < 20 and rain != {}:
        return 'Судя по погоде, лучше надень штаны и кофту. И не забудь зонт, сейчас же дождь!'
    elif temp > 7 and temp < 15 and rain == {}:
        return 'Сейчас достаточно холодно, лучше надень куртку'
    elif temp > 7 and temp < 15 and rain != {}:
        return 'Сейчас достаточно холодно, лучше надень куртку. И не забудь зонт, сейчас же дождь!'
    elif temp >= 0 and temp <= 7 and rain == {}:
        return 'Сейчас холодно, надень тёплую куртку'
    elif temp >= 0 and temp <= 7 and rain != {}:
        return 'Сейчас холодно, надень тёплую куртку. И не забудь зонт, сейчас же дождь!'
    elif temp < 0:
        return 'Сейчас очень холодно, надень пуховик или теплую куртку'
    elif temp >= 20:
        return 'Сейчас жарко, надень шорты с футболкой'

output_data = ["12"]
json_data = dict()

@eel.expose
def update_messages():
    print(output_data)
    return output_data[-1]

@eel.expose
def main(gpt_request, gpt_code, google_request, dialog, is_active_command, weather):
    with sd.RawInputStream(
            samplerate=samlerate,
            blocksize=8000,
            device=device,
            dtype='int16',
            channels=1,
            callback=callback):

        rec = vosk.KaldiRecognizer(model, samlerate)

        count = 1
        print( "[INFO] Говорите..." )




        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                print(" ")
                print(count)
                result = rec.Result()
                i = 14
                word = ""
                while True:

                    try:
                        if result[i] == '"': # define end of phrase
                            break
                        word += result[i]
                        i+=1

                    except Exception as _ex:
                        print(_ex)
                        break

                print(word)
                if word != "":
                    output_data.append(word)
                    key = str(str(count) + "user")
                    json_data[key] = word
                    with open('web/file.json', 'w') as json_file:
                        json.dump(json_data, json_file)
                    #update_messages()

                # else: pass
                # here i`ll write logic of my program

                if "гугл" in word:
                    webbrowser.open("https://www.google.com")
                    is_active_command = True
                    output_data.append("Выполняю")
                    key_ai = str(count) + "ai"
                    json_data[key_ai] = "Выполняю"
                    with open('web/file.json', 'w') as json_file:
                        json.dump(json_data, json_file)
                    #update_messages()
                elif "ютуб" in word:
                    webbrowser.open("https://www.youtube.com/")
                    is_active_command = True
                    output_data.append("Выполняю")
                    key_ai = str(count) + "ai"
                    json_data[key_ai] = "Выполняю"
                    with open('web/file.json', 'w') as json_file:
                        json.dump(json_data, json_file)
                    #update_messages()
                elif "почту" in word or "почта" in word:
                    webbrowser.open("https://mail.google.com/mail/u/0/#inbox")
                    is_active_command = True
                    output_data.append("Выполняю")
                    key_ai = str(count) + "ai"
                    json_data[key_ai] = "Выполняю"
                    with open('web/file.json', 'w') as json_file:
                        json.dump(json_data, json_file)
                    #update_messages()
                elif "линкедин" in word:
                    webbrowser.open("https://www.linkedin.com")
                    is_active_command = True
                    output_data.append("Выполняю")
                    key_ai = str(count) + "ai"
                    json_data[key_ai] = "Выполняю"
                    with open('web/file.json', 'w') as json_file:
                        json.dump(json_data, json_file)
                    #update_messages()
                elif "блокнот" in word:
                    subprocess.Popen(['notepad.exe'])
                    is_active_command = True
                    output_data.append("Выполняю")
                    key_ai = str(count) + "ai"
                    json_data[key_ai] = "Выполняю"
                    with open('web/file.json', 'w') as json_file:
                        json.dump(json_data, json_file)
                    #update_messages()
                elif "спящий режим" in word or "выключись" in word:
                    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
                elif "выключи систему" in word:
                    os.system("shutdown /s /t 1")
                elif "выключи браузер" in word or "закрой браузер"in word:
                    process_name = "chrome.exe"
                    os.system(f"taskkill /f /im {process_name}")
                    is_active_command = True
                # add castom commands

                # finish simple commands

                # activate and disactivate dialog mode

                elif word == "привет бедолага" or word == "бедолага привет":
                    print("[INFO] Dialog mode is active")
                    dialog = True
                    engine.say("Привет лошпедик")
                    engine.runAndWait()
                    is_active_command = True
                    output_data.append("Привет лошпедик")
                    key_ai = str(count) + "ai"
                    json_data[key_ai] = "Привет лошпедик"
                    with open('web/file.json', 'w') as json_file:
                        json.dump(json_data, json_file)
                    #update_messages()

                elif word == "пока бедолага" or word == "бедолага пока":
                    dialog = False
                    engine.say("Иди в попу, сам ты бедолага")
                    engine.runAndWait()
                    print("[INFO] Finish dialog mode")
                    output_data.append("Иди в попу, сам ты бедолага")
                    key_ai = str(count) + "ai"
                    json_data[key_ai] = "Иди в попу, сам ты бедолага"
                    with open('web/file.json', 'w') as json_file:
                        json.dump(json_data, json_file)
                    #update_messages()


                # make search view for assistant
                # remove key words of the message
                elif "бедолага ищи" in word:
                    is_active_command = True
                    if "бедолага ищи" == word:

                        google_request = True
                        output_data.append("Я вас слушаю")
                        key_ai = str(count) + "ai"
                        json_data[key_ai] = "Я вас слушаю"
                        with open('web/file.json', 'w') as json_file:
                            json.dump(json_data, json_file)
                        #update_messages()
                        print("Я вас слушаю")

                    else:
                        cut_words = ['бедолага ищи ']
                        search_request = word[:]
                        for el in cut_words:
                            search_request = search_request.replace(el, "", 1)

                        request_google = "https://www.google.com/search?q=" + search_request + "&num=10" + "&hl=ru"
                        webbrowser.open(request_google)
                        key_ai = str(count) + "ai"
                        json_data[key_ai] = "Выполняю"
                        with open('web/file.json', 'w') as json_file:
                            json.dump(json_data, json_file)
                        #update_messages()

                elif google_request:
                    request_google = "https://www.google.com/search?q=" + word + "&num=10" + "&hl=ru"
                    webbrowser.open(request_google)
                    google_request = False
                    is_active_command = True
                    output_data.append("Выполняю")
                    key_ai = str(count) + "ai"
                    json_data[key_ai] = "Выполняю"
                    with open('web/file.json', 'w') as json_file:
                            json.dump(json_data, json_file)
                    #update_messages()


                elif ("погода" in word or "погоду" in word) and  "бедолага" in word:
                    weather = True
                    engine.say("В каком городе?")
                    engine.runAndWait()
                    key_ai = str(count) + "ai"
                    json_data[key_ai] = "В каком городе?"
                    with open('web/file.json', 'w') as json_file:
                            json.dump(json_data, json_file)
                elif weather:
                    city = word
                    owm = OWM('a99a76ecfd5f4739737d50a7f8604843')
                    mgr = owm.weather_manager()
                    observation = mgr.weather_at_place(city)
                    w = observation.weather
                    t = w.temperature('celsius') ['temp']
                    r = w.rain
                    o = ""
                    if r == {}:
                        o = "Сейчас дождя нет"

                    res = weather_func(t, r)
                    weather = False
                    engine.say(f"Сейчас {t} градусов. {res}. {o}")
                    engine.runAndWait()
                    output_data.append(f"Сейчас {t} градусов. {res}. {o}")
                    key_ai = str(count) + "ai"
                    json_data[key_ai] = f"Сейчас {t} градусов. {res}. {o}"
                    with open('web/file.json', 'w') as json_file:
                            json.dump(json_data, json_file)
                    #update_messages()

                # using chat gpt api

                # remove key words of the message
                elif "бедолага скажи" in word and "погод" not in word:
                    if "бедолага скажи" == word:
                        gpt_request = True
                        output_data.append("yes")
                        key_ai = str(count) + "ai"
                        json_data[key_ai] = "Выполняю"
                        with open('web/file.json', 'w') as json_file:
                            json.dump(json_data, json_file)
                        #update_messages()
                    else:
                        cut_words_chat = ['бедолага скажи ']
                        request_chatgpt_text = word[:]
                        for el in cut_words_chat:
                            request_chatgpt_text = request_chatgpt_text.replace(el, "", 1)

                        requets_chatgpt = openai.Completion.create(
                            engine=model_engine,
                            prompt=request_chatgpt_text,
                            max_tokens=2048,
                            temperature=0.5,
                            top_p=1,
                            frequency_penalty=0,
                            presence_penalty=0
                        )

                        print("Бедолага отвечает на вопрос...")
                        engine.say(requets_chatgpt.choices[0].text)
                        engine.runAndWait()
                        is_active_command = True
                        output_data.append(requets_chatgpt.choices[0].text)
                        key_ai = str(count) + "ai"
                        json_data[key_ai] = requets_chatgpt.choices[0].text
                        with open('web/file.json', 'w') as json_file:
                            json.dump(json_data, json_file)
                        #update_messages()



                elif gpt_request:
                    requets_chatgpt = openai.Completion.create(
                        engine=model_engine,
                        prompt=word,
                        max_tokens=2048,
                        temperature=0.5,
                        top_p=1,
                        frequency_penalty=0,
                        presence_penalty=0
                    )

                    print("Бедолага отвечает на вопрос...")
                    print(requets_chatgpt.choices[0].text)
                    gpt_request = False
                    is_active_command = True
                    output_data.append(requets_chatgpt.choices[0].text)
                    key_ai = str(count) + "ai"
                    json_data[key_ai] = requets_chatgpt.choices[0].text
                    with open('web/file.json', 'w') as json_file:
                            json.dump(json_data, json_file)
                    #update_messages()

                # chat gpt code
                elif "бедолага помоги" in word:
                    is_active_command = True
                    if "бедолага помоги" == word:

                        gpt_code = True
                        output_data.append("говорите")
                        key_ai = str(count) + "ai"
                        json_data[key_ai] = "говорите"
                        with open('web/file.json', 'w') as json_file:
                            json.dump(json_data, json_file)
                        #update_messages()


                    else:
                        cut_key_word = ["бедолага помоги "]
                        text_request = word[:]
                        for el in cut_key_word:
                            text_request = text_request.replace(el, "", 1)

                        request_code_chatgpt = openai.Completion.create(
                            engine=model_engine,
                            prompt=word,
                            max_tokens=2048,
                            temperature=0.5,
                            top_p=1,
                            frequency_penalty=0,
                            presence_penalty=0
                        )


                        text_result = request_code_chatgpt.choices[0].text

                        try:
                            with open(config.path, "w", encoding="utf-8") as file:
                                file.write(text_result)
                            file.close()
                        except Exception as _ex:
                            print(_ex)

                        try:
                            with open(config.path, "r+") as f:
                                lines = f.readlines()

                                new_lines = []
                                for line in lines:
                                    if is_valid_line(line):
                                        new_lines.append(line)

                                f.seek(0)
                                f.write("".join(new_lines))
                                f.truncate()

                        except Exception as _ex:
                            print(_ex)
                        output_data.append("проверяй")
                        key_ai = str(count) + "ai"
                        json_data[key_ai] = "проверяй"
                        with open('web/file.json', 'w') as json_file:
                            json.dump(json_data, json_file)
                        #update_messages()


                elif gpt_code:
                    gpt_code = False

                    request_code_chatgpt = openai.Completion.create(
                        engine=model_engine,
                        prompt=word + text_result,
                        max_tokens=2048,
                        temperature=0.5,
                        top_p=1,
                        frequency_penalty=0,
                        presence_penalty=0
                    )


                    text_result = request_code_chatgpt.choices[0].text

                    try:
                        with open(config.path, "w", encoding="utf-8") as file:
                            file.write(text_result)
                        file.close()
                    except Exception as _ex:
                        print(_ex)

                    try:
                        with open(config.path, "r+") as f:
                            lines = f.readlines()

                            new_lines = []
                            for line in lines:
                                if is_valid_line(line):
                                    new_lines.append(line)

                            f.seek(0)
                            f.write("".join(new_lines))
                            f.truncate()

                    except Exception as _ex:
                        print(_ex)
                    is_active_command = True
                    output_data.append("проверяй")
                    key_ai = str(count) + "ai"
                    json_data[key_ai] = "проверяй"
                    with open('web/file.json', 'w') as json_file:
                            json.dump(json_data, json_file)
                    #update_messages()

                # make screenshots
                elif "бедолага" in word and "скриншот" in word:
                    screenshot = pyautogui.screenshot()
                    file_name = "screenshot"+str(count)+".png"
                    screenshot.save(file_name)
                    print("Ваш скриншот сохранен по данной директории")
                    is_active_command = True
                    output_data.append("Ваш скриншот сохранен по данной директории")
                    key_ai = str(count) + "ai"
                    json_data[key_ai] = "Скриншот сделан"
                    with open('web/file.json', 'w') as json_file:
                            json.dump(json_data, json_file)
                    #update_messages()


                elif "заверши" in word and "работу" in word and "бедолага" in word:
                    json_data.clear()
                    json_data['end'] = "empty"
                    with open('web/file.json', 'w') as json_file:
                        json.dump(json_data, json_file)
                    request = ('netsh firewall set portopening tcp 5000 smb disable') # здесь код для открытия или закрытия портов
                    code = os.system(request)
                    print(code)
                    sys.exit()
                    break

                # make dialog function
                if dialog and word != "" and not is_active_command:
                    try:
                        answer = dialog_gpt(word)
                        print(answer)
                        output_data.append(answer)
                        key_ai = str(count) + "ai"
                        json_data[key_ai] = answer
                        with open('web/file.json', 'w') as json_file:
                            json.dump(json_data, json_file)
                        #update_messages()
                        engine.say(answer)
                        engine.runAndWait()
                        # print(dialogue_history)
                    except Exception as _ex:
                        # engine.say(str(_ex))
                        # engine.runAndWait()
                        output_data.append(str(_ex))
                        key_ai = str(count) + "ai"
                        json_data[key_ai] = str(_ex)
                        with open('web/file.json', 'w') as json_file:
                            json.dump(json_data, json_file)
                        #update_messages()

                count+=1
                is_active_command = False


def go_script(port):
    eel.init("web")
    eel.start("main.html", size=(470, 600), port=port)

# go_script(randint(1000, 7999))
go_script(5000)

# if __name__ == "__main__":
#     main(gpt_request, gpt_code, google_request, dialog, is_active_command, weather)

