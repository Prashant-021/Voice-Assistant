from ntpath import join
from subprocess import SW_HIDE
import time
import sys
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import pywhatkit as kit
import pyautogui
import pyjokes
from PyQt5 import QtWidgets,QtCore,QtGui
from PyQt5.QtCore import QTimer,QTime,QDate,Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from voiceassistantgui import Ui_VoiceAssistant

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("good morning")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon")

    else:
        speak("good evening")

    speak("How May I help you")

class MainThread(QThread):
    def __init__(self):
        super(MainThread,self).__init__()

    def run(self):
        self.taskExecution()

    def takeCommand(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            audio = r.listen(source,timeout=1,phrase_time_limit=5)

        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")

        except Exception as e:
            print(e)
            print("Say that again please....")
            speak("Say that again please....")
            return "none"
        query = query.lower()
        return query

    def taskExecution(self):
        wishMe()
        while True:
            
            self.query = self.takeCommand()

            if 'wikipedia' in self.query:
                speak('Searching Wikipedia....')
                query = query.replace("wikiepedia", "")
                results = wikipedia.summary(query, sentences=2)
                speak("According to wikipedia")
                print(results)
                speak(results)

            elif 'open youtube' in self.query:
                speak("what should i search on youtube")
                cm = self.takeCommand()
                kit.playonyt(f"{cm}")

            elif 'open google' in self.query:
                chromepath = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
                os.startfile(chromepath)

            elif 'play music' in self.query:
                    music_dir = 'D:\\songs'
                    songs = os.listdir(music_dir)
                    print(songs)
                    os.startfile(os.path.join(music_dir, songs[0]))

            elif 'the time' in self.query:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"Time is {strTime}")
            
            elif 'open notepad' in self.query:
                codePath = "C:\\Windows\\system32\\notepad.exe"
                os.startfile(codePath)

            elif 'close notepad' in self.query:
                speak("Closing Notepad")
                os.system("taskkill /f /im notepad.exe")

            elif 'open code' in self.query:
                codePath = "D:\\VSCode\\Microsoft VS Code\\Code.exe"
                os.startfile(codePath)
            
            elif 'close code' in self.query:
                speak("Okay Closing VSCode")
                os.system("taskkill /f /im Code.exe")

            elif 'open whatsapp' in self.query:
                speak("opening whatsapp")
                whatsapppath = "C:\\Users\\PRASHANT PATEL\\AppData\\Local\\WhatsApp\\WhatsApp.exe"
                os.startfile(whatsapppath)
                time.sleep(5)

            elif 'close whatsapp' in self.query:
                speak("closing whatsapp")
                os.system("taskkill /f /im WhatsApp.exe")

            elif 'volume up' in self.query:
                pyautogui.press("volumeup" , 10)
            
            elif 'volume down' in self.query:
                pyautogui.press("volumedown" , 5)
            
            elif 'volume mute' in self.query:
                pyautogui.press("volumemute")

            # elif 'do some calculations' in self.query:
            #     val1 = int(takeCommand())
            
            elif 'tell me a joke' in self.query:
                joke = pyjokes.get_joke()
                speak(joke)

            elif 'show all windows' in self.query:
                with pyautogui.hold('win'):
                    pyautogui.press('tab')
            
            elif 'shutdown the system' in self.query:
                os.system("shutdown /s /t 5")
            
            
            elif 'go to sleep' in self.query:
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

            elif "no" in self.query:
                speak("thank you, have a nice day")
                sys.exit()

            speak("Do you have any other work")

startExecution = MainThread()

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_VoiceAssistant()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)
    
    def startTask(self):
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        startExecution.start()

    def showTime(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        label_time = current_time.toString('hh:mm:ss')
        label_date = current_date.toString(Qt.ISODate)
        self.ui.textBrowser.setText(label_date)
        self.ui.textBrowser_2.setText(label_time)
        

app = QApplication(sys.argv)
VoiceAssistant = Main()
VoiceAssistant.show()
exit(app.exec_())

