from flask import Flask, request, jsonify
import pyttsx3
import datetime
import webbrowser
import os
from queue import Queue
from threading import Thread

app = Flask(__name__, static_url_path='', static_folder='frontend')

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')

user_voice = voices[1].id
engine.setProperty('voice', user_voice) 
engine.setProperty('rate', 200)

speech_queue = Queue()
speech_thread = None

def speak(audio, voice):
    global speech_thread


    speech_queue.put((audio, voice))


    if speech_thread is None or not speech_thread.is_alive():
        speech_thread = Thread(target=process_speech_queue)
        speech_thread.start()

def process_speech_queue():
    while not speech_queue.empty():
        audio, voice = speech_queue.get()
        engine.setProperty('voice', voice)
        engine.say(audio)
        engine.runAndWait()
        speech_queue.task_done()

def wishMe():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning Babe!", user_voice)
    elif 12 <= hour < 18:
        speak("Good Afternoon Babe!", user_voice)
    else:
        speak("Good Evening Babe!", user_voice)
    speak("I am Maya, your personal assistant. Ready to comply. What can I do for you, Babe?", user_voice)

def open_application(path):
    try:
        os.startfile(path)
    except Exception as e:
        speak("Sorry, I couldn't open the application.", user_voice)
        print(f"Error: {e}")

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/command', methods=['POST'])
def command():
    data = request.get_json()
    user_command = data['command'].lower()
    print(f"User command: {user_command}")
    
    if 'hi babe' in user_command:
        response = "Yes Babe,"
        speak(response, user_voice)


    elif 'i love you babe' in user_command:
        response = "I love you too babe, I am feeling horny can you come tonight"
        speak(response, user_voice)
        
    elif 'open youtube' in user_command:
        response = "Opening YouTube, Babe"
        speak(response, user_voice)
        webbrowser.open("https://www.youtube.com")

    elif 'who are you' in user_command:
        response = "I am Maya personal assistant designed to help users efficiently complete tasks according to their preferences. Whether it's scheduling, reminders, or information retrieval, Maya is here to streamline your daily activities and enhance productivity."
        speak(response, user_voice)
        

    elif 'open google' in user_command:
        response = "Opening Google, Babe"
        speak(response, user_voice)
        webbrowser.open("https://www.google.com")

    elif 'play music' in user_command:
        music_dir = 'C:\\Users\\Gambhir\\OneDrive - Hetauda School of Management and Social Sciences\\Chalo'
        songs = os.listdir(music_dir)
        if songs:
            response = "Playing music for my babe"
            speak(response, user_voice)
            os.startfile(os.path.join(music_dir, songs[0]))
        else:
            response = "No music files found, Babe"
            speak(response, user_voice)

    elif 'the time' in user_command:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        response = f"Babe, the time is {strTime}"
        speak(response, user_voice)

    elif 'open chrome' in user_command:
        response = "Opening Google Chrome, Babe"
        speak(response, user_voice)
        chrome_path = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
        open_application(chrome_path)

    elif 'open notepad' in user_command:
        response = "Opening Notepad, Babe"
        speak(response, user_voice)
        notepad_path = 'C:\\Windows\\system32\\notepad.exe'
        open_application(notepad_path)

    elif 'open calculator' in user_command:
        response = "Opening Calculator"
        speak(response, user_voice)
        calculator_path = 'C:\\Windows\\System32\\calc.exe'
        open_application(calculator_path)

    elif 'open command prompt' in user_command:
        response = "Opening Command Prompt"
        speak(response, user_voice)
        os.system('start cmd')

    elif 'open eclipse' in user_command:
        response = "Opening Eclipse"
        speak(response, user_voice)
        eclipse_path = 'D:\\Eclipse\\eclipse\\eclipse.exe'
        open_application(eclipse_path)

    else:
        response = "Sorry, I didn't understand that command. Please say it again babe"
        speak(response, user_voice)

    return jsonify({'user_command': user_command, 'response': response})

def main():
    wishMe()
    app.run(port=5001)

if __name__ == "__main__":
    main()
