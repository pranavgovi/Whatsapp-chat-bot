from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
import requests
import json
import pyaudio
import pyttsx3
import speech_recognition as sr
import re
import pandas as pd



@app.route('/bot', methods=['POST'])

def bot():
    #quote=''
    text = request.values.get('Body', '').lower() #gets whatsapp message
    dataframe1 = pd.read_excel('covid.xlsx')
    country = dataframe1['Country/Region'].tolist()
    death_list = dataframe1['Deaths'].tolist()
    name = ['pranav', 'rengaraj','varsha','kaavya','ipshita']
    def sayhello(name):
        return ("hello {} what can i do for u".format(name))
    user_pattern = {
        re.compile("[\w\s]+bot [\w\s]+"): lambda name: sayhello(name)

    }
    for pattern, func in user_pattern.items():
        if pattern.match(text):
            namess = text.split()
            for i in name:
                if i.lower() in namess:
                    quote = func(i)
    def special():
        x="i provide  stats about covid 19...wanna know?"
        return x
    speciality = {
        re.compile("[\w\s]+speciality"): special,
        re.compile("what do you do"): special
    }
    for pattern, func in speciality.items():
        if pattern.match(text):
            quote = func()




    def provide_details():
        p = ["i can provide country wise covid data",
             "i can provide you  the exact number of deaths in  a particular country ",
             "i can also list the active cases", "common ask one question"]
        return p

    def get_country(death):
        for i in range(len(death_list)):
            if (str(death_list[i]) == str(death)):
                return country[i]

    def highactive_count():

        high = dataframe1['Active'].tolist()
        max = high[0]
        need = 0
        for i in range(len(high)):
            if (high[i] > max):
                max = high[i]
                need = i
        return country[need]

    def lowactive_count():

        high = dataframe1['Active'].tolist()
        max = high[0]
        need = 0
        for i in range(len(high)):
            if (high[i] < max):
                min = high[i]
                need = i
        return country[need]

    def highdeath_country():
        max = 0
        need = 0

        for i in range(len(death_list)):
            if (death_list[i] > max):
                max = death_list[i]
                need = i
        return country[need]

    def lowdeath_country():
        max = death_list[0]
        need = 0

        for i in range(len(death_list)):
            if (max > death_list[i]):
                max = death_list[i]
                need = i
        return country[need]

    def high_per():
        high = dataframe1['Deaths / 100 Cases'].tolist()
        x = high[0]
        ind = 0
        for i in range(len(high)):
            if (high[i] > x):
                x = high[i]
                ind = i
        return country[ind]

    def low_per():
        high = dataframe1['Deaths / 100 Cases'].tolist()
        x = high[0]
        ind = 0
        for i in range(len(high)):
            if (high[i] < x):
                x = high[i]
                ind = i
        return country[ind]

    end_pharse = "stop"
    country_pattern = {

        re.compile(r"[a-zA-Z]+ country [a-zA-Z]+ [0-9][0-9][0-9][0-9] deaths", re.IGNORECASE): lambda
            death: get_country(death)
        # re.compile("[\w\s]+ year [0-9][0-9[0-9][0-9]+[\w\s]+world cup"): lambda year: s.get_team(death)

    }
    high_active = {
        re.compile(r"[\w\s]+ highest +[\w\s]+active [\w\s]+", re.IGNORECASE): highactive_count,
        re.compile(r"[\w\s]+ highest active [\w\s]+", re.IGNORECASE): highactive_count

    }
    low_active = {
        re.compile(r"[\w\s]+ lowest +[\w\s]+active [\w\s]+", re.IGNORECASE): lowactive_count,
        re.compile(r"[\w\s]+ lowest active [\w\s]+", re.IGNORECASE): lowactive_count

    }
    highestdeathpercases = {
        re.compile(r"[\w\s]+ highest +[\w\s]+per 100 [\w\s]+", re.IGNORECASE): high_per,
        re.compile(r"[\w\s]+ highest +[\w\s]+per hundred [\w\s]+", re.IGNORECASE): high_per

    }
    lowestdeathpercases = {
        re.compile(r"[\w\s]+ lowest +[\w\s]+per 100 [\w\s]+", re.IGNORECASE): low_per,
        re.compile(r"[\w\s]+ lowest +[\w\s]+per hundred [\w\s]+", re.IGNORECASE): low_per

    }
    highdeath_pattern = {
        re.compile(r"[\w\s]+ highest [\w\s]+ deaths", re.IGNORECASE): highdeath_country,
        re.compile(r"[\w\s]+ highest deaths", re.IGNORECASE): highdeath_country,
        re.compile("highest deaths"): highdeath_country



    }
    lowdeath_pattern = {
        re.compile(r"[\w\s]+ lowest [\w\s]+ deaths", re.IGNORECASE): lowdeath_country,
        re.compile(r"[\w\s]+ lowest deaths", re.IGNORECASE): lowdeath_country,
        re.compile("lowest deaths"): lowdeath_country

    }
    respond_pattern = {
        re.compile("yes"): provide_details
    }
    key = None
    for pattern, func in country_pattern.items():
        if pattern.match(text):
            yearsss = text.split()
            for death_count in death_list:
                if str(death_count) in yearsss:
                    quote = func(str(death_count))



    for pattern, func in highestdeathpercases.items():
        if pattern.match(text):
            quote = func()


    for pattern, func in lowestdeathpercases.items():
        if pattern.match(text):
            quote = func()

    for pattern, func in respond_pattern.items():
        if pattern.match(text):
            key = func()
            quote=' '.join(key)






    for pattern, func in high_active.items():
        if pattern.match(text):
            quote = func()

    for pattern, func in highdeath_pattern.items():
        if pattern.match(text):
            quote = func()

    for pattern, func in lowdeath_pattern.items():
        if pattern.match(text):
            quote = func()


    for pattern, func in low_active.items():
        if pattern.match(text):
            quote = func()


    # if key:
    #     print(key)
    #     speak(key)
    # if text.find(end_pharse) != -1:
    #     break

    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    if(len(quote)==0):
        quote="fault"

    # if 'greet' in text:
    #
    #     # return a quote
    #     # death_list = dataframe1['Deaths'].tolist()
    #     # quote=str(death_list[0])
    # else:
    #     quote = 'I could not retrieve a quote at this time, sorry.'
    msg.body(quote)

    return str(resp)
if __name__ == '__main__':
    app.run()
