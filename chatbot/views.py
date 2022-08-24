from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from tensorflow import keras
import json
import pickle
import nltk
from nltk.stem import WordNetLemmatizer
import numpy as np
import speech_recognition as sr
import pyttsx3
import random


lemmatizer = WordNetLemmatizer()
data = pickle.load( open( "chatbot/training_data", "rb" ) )
words = data['words']
classes = data['classes']
train_x = data['train_x']
train_y = data['train_y']
model = keras.models.load_model('chatbot/chatbot_model.h5')
with open('chatbot/intents.json') as json_data:
    intents = json.load(json_data)
# Create your views here.


def clean_up_sentence(sentence):
    # tokenize the pattern
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words
def bow(sentence, words, show_details=False):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)

    return(np.array(bag))

def predict_class(sentence, model=model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.8
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list


def getResponse(sentence):
    results = predict_class(sentence)
        # loop as long as there are matches to process
    if (results):
        for i in intents['intents']:
                # find a tag matching the first result
            if i['tag'] == results[0]['intent']:
                print("My tag",i['tag'])
                    # a random response from the intent
                result = random.choice(i['responses'])
                break;
            else :
                result ="i didn't understand Retype your question"
    else :
        result ="i didn't understand Retype your question"

    return result


x=predict_class('ZANEXTRA 20 mg / 20 mg 30 CP FSP')
print(x)
def chatbot_response(msg):
    res = getResponse(msg)
    return res




def home (request):
   
    return render(request, 'bot/index.html')

def chatbotResponse(request):
    print('AJAX working')
    if request.method == 'POST':
        print('INside POST')
        the_question= request.POST['question']
        print('Question',the_question)
        response = chatbot_response(the_question)
        print('response',response)

 
    return JsonResponse ({"response": response },safe=False)
   
   
def soundResponse1(request):
    print('AJAX sound working')
    a = sr.Recognizer()
    mic = sr.Microphone()

    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', 175)

    volume = engine.getProperty('volume')
    engine.setProperty('volume', 1.0)

    voices = engine.getProperty('voices')

    engine.say("HELLO USER ! I AM bottrainer , YOUR PERSONAL  CHAT BOT . PLEASE TELL ME YOUR question")
    engine.runAndWait()

        
    while True or final.lower()=='yes':
        with mic as source:
            print("ask your question")
            engine.say("You may tell me your question now")
            engine.runAndWait()
            print('asef 1')
            audio = a.listen(source)
            print('asef 2')
            try:
                audio = a.listen(source)
                print('asef 3')
                text = a.recognize_google(audio)
                print('asef 4')
                engine.say("You said {}".format(text))
                print('asef 5')
                engine.runAndWait()
                print('asef 6')
                ints = predict_class(text)
                print('asef 7')
                res = getResponse(ints,intents)
                print('asef 8')

                engine.say(res)
                print('asef 9')
                engine.runAndWait()
                print('asef 10')
                print("You said : " ,text)
                print('asef 11')
                print("Result : ", res)
                print('asef 12')
            except sr.UnknownValueError:
                engine.say("Sorry I didn't understand your question . Please tell me again")
                engine.runAndWait()
                print("Sorry couldn't understand that")
            finally:    
                engine.say("Do you want to Continue")
                engine.runAndWait()
        
        with mic as ans:
            voice = a.listen(ans)
            final = a.recognize_google(voice)

        if final.lower()=='no' or final.lower()=='exit':
            engine.say("Thank You for using me . Exiting Now ")
            engine.runAndWait()
            print("Bot has been stopped by the user")
            break



    return JsonResponse ({"response": "response" },safe=False)




def get_response(intents_list,intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    
    for i in list_of_intents:
        if i['tag'] == tag :
            result = random.choice(i['responses'])
            break
    return result

def soundResponse(request):
    print("Bot is Running")

    a = sr.Recognizer()
    mic = sr.Microphone()

    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', 175)

    volume = engine.getProperty('volume')
    engine.setProperty('volume', 1.0)

    voices = engine.getProperty('voices')

    engine.say("HELLO USER ! I AM bottrainer , YOUR PERSONAL  CHAT BOT .")
    engine.runAndWait()


    while True or final.lower()=='yes':
        with mic as source:
            print("ask your question")
            engine.say("You may tell me your question now")
            engine.runAndWait()
            try:
                audio = a.listen(source)
                text = a.recognize_google(audio)
                engine.say("You said {}".format(text))
                engine.runAndWait()
                ints = predict_class(text)
                res = get_response(ints,intents)
                engine.say(res)
                engine.runAndWait()
                print("You said : " ,text)
                print("Result : ", res)
            except sr.UnknownValueError:
                engine.say("Sorry I didn't understand your question . Please tell me again")
                engine.runAndWait()
                print("Sorry couldn't understand that")
            finally:    
                engine.say("Do you want to Continue")
                engine.runAndWait()
    
        with mic as ans:
            voice = a.listen(ans)
            final = a.recognize_google(voice)

        if final.lower()=='no' or final.lower()=='exit':
            engine.say("Thank You for using me . Exiting Now ")
            engine.runAndWait()
            print("Bot has been stopped by the user")
            break
    return JsonResponse ({"response": "response" },safe=False)