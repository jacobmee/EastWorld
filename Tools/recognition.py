# -*- coding: utf-8 -*-

import PyBaiduYuyin as pby
from gtts import gTTS
import speech_recognition as sr
import os
from os import path
import urllib2
import sys
import json

apiKey = "QUQgAhhdfODY9KbaR7928pHN"
secretKey = "f994c8815ddef688325fe3be89ffc3d5"
GOOGLE_KEY = "AIzaSyAcalCzUvPmmJ7CZBFOEWx2Z1ZSn4Vs1gg"

btts = pby.TTS(app_key=apiKey, secret_key=secretKey)
btts.say("你说")

# obtain audio from the microphone
gr = sr.Recognizer()
gm = sr.Microphone(sample_rate=16000)
#gm.RATE = 16000
#m.CHUNK = 512

br = pby.Recognizer()
bm = pby.Microphone()

use_Google = False
use_Baidu = True

use_wav = True
use_listen = False




while True:

    text = ""
    # Try google first if can't access, always use Baidu
    if use_Google :



        audio = None

        os.system('arecord -f S16_LE -r 16000 -d 3 -D plughw:0,0 temp.wav')
        AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "temp.wav")
        with sr.AudioFile(AUDIO_FILE) as source:
            audio = gr.record(source)  # read the entire audio file


        '''with gm as source:
            print("Say something!")
            audio = gr.listen(source)'''

        # recognize speech using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            result = gr.recognize_google(audio, GOOGLE_KEY, language="zh-CN")
            print("Google Speech Recognition thinks you said " + result)

            text = result.encode('utf-8').strip()

        except sr.UnknownValueError:
            print("Google Speech Recogni/tion could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

    if use_Baidu :

        #with bm as source:
        #    br.adjust_for_ambient_noise(source) # listen for 1 second to calibrate the energy threshold for ambient noise levels
        #    audio = br.listen(source)

        os.system('arecord -f S16_LE -r 16000 -d 3 -D plughw:0,0 temp.wav')
        AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "temp.wav")
        with pby.WavFile(AUDIO_FILE) as source:
            audio = br.record(source)  # read the entire audio file

        # instead of `r.recognize_google(audio, show_all=True)`
        result = br.recognize(audio)
        text = result.encode('utf-8').strip()

    print "Recognized: %s" % text

    if text == "知道我在哪里么":
        print "发现你了"
        continue

    if text != "":
        url = "http://apis.baidu.com/turing/turing/turing?"
        key = "879a6cb3afb84dbf4fc84a1df2ab7319"
        userid = "1000"
        api_key = "64c2b023d27eb2ffe1dcef2ac7b70e1b"

        # words = urllib2.Parse.quote(words)
        url = url + "key=" + key + "&info=" + text + "&userid=" + userid

        req = urllib2.Request(url)
        req.add_header("apikey", api_key)

        print("robot start request")
        resp = urllib2.urlopen(req)
        print("robot stop request")
        content = resp.read()

        if content:
            data = json.loads(content.decode("utf-8"))
            answer = data["text"]

    print "Answered: %s" % answer

    if answer == "":
        answer = "没听到"
    else:
        answer = answer.encode('utf-8').strip()

    if use_Google:
        audio_file = "temp.mp3"
        gtts = gTTS(answer, lang="zh-cn")
        gtts.save(audio_file)
        os.system('mpg123 "%s"' % audio_file)

    if use_Baidu:
        # print resultTmp[u'alternative'], type(resultTmp[u'alternative'])
        btts.say(answer)