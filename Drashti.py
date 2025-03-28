import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import requests
from gnews import GNews
from groq import Groq
from groq import Client
import file_operations as fo
from app_open import open_application,close_application
import googlesearch   

class Jarvis:
    def __init__(self):
        self.engine = pyttsx3.init('sapi5')
        self.engine.setProperty('voice', self.engine.getProperty('voices')[1].id)
        self.sleep_mode = False
        self.weather_api_key='209b819bd7c3a8fa3810d0c44aa10b48'
        self.news_api_key='8b01d20f25e9436a953672b18c574845'
        self.command_log_file = "commands.txt"
        self.additional_commands_dict = {
            "who created you": "I was created by a Jarnil Patel.",
            "what can you do": "I can perform various tasks like searching, playing music, and answering your questions.",
            "tell me a joke": "Why don’t scientists trust atoms? Because they make up everything!",
            "what is the capital of india": "The capital of India is Delhi.",
            "what is your name":"My Name Is Drashti, I Am a Vertual Voice Assistance",
            "how are you": "I am just a program, but I am functioning as expected!",
            "define artificial intelligence": "Artificial Intelligence is the simulation of human intelligence in machines that are programmed to think like humans and mimic their actions.",
            "what is you country":"i am just a Program, howevre my devloper belongs from India"
        }

    def speak(self, audio):
        self.engine.say(audio)
        self.engine.runAndWait()

    def greet(self):
        hour = int(datetime.datetime.now().hour)
        if hour < 12:
            self.speak("Good Morning!")
        elif hour < 18:
            self.speak("Good Afternoon!")
        else:
            self.speak("Good Evening!")
        self.speak("I am Drashti. How may I assist you today?")

    def take_command(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.pause_threshold = 1
            recognizer.energy_threshold = 300
            audio = recognizer.listen(source, timeout=None, phrase_time_limit=None)
            try:
                print("Recognizing...")
                query = recognizer.recognize_google(audio, language='en-in')
                print(f"User said: {query}\n")
                return query.lower()
            except Exception:
                print("Please say that again...")
                return "none"

    def log_command(self, command):
        with open(self.command_log_file, "a") as file:
            file.write(command + "\n")

    def search_wikipedia(self, query):
        self.speak('Searching Wikipedia...')
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        self.speak("According to Wikipedia")
        print(results)
        self.speak(results)
        self.log_command(query)
        
    def get_weather(self, city):
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.weather_api_key}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            weather = data['weather'][0]['description']
            temp = data['main']['temp']
            print(f"The weather in {city} is {weather} with a temperature of {temp} degrees Celsius.")
            self.speak(f"The weather in {city} is {weather} with a temperature of {temp} degrees Celsius.")
        else:
            self.speak("Sorry, I couldn't fetch the weather information.")
            
    def fetch_news(self):
        google_news = GNews(language='en', country='IN', max_results=5)
        india_news = google_news.get_top_news()
        self.speak("Here are the top headlines from India:")
        for article in india_news:
            self.speak(article['title'])
            
    def open_website(self, site):
        site = site.replace(" ", "")  
        self.speak(f"Opening {site}")
        webbrowser.open(f"https://{site}.com")
        self.log_command(f"open {site}")

    def play_music(self):
        music_dir = 'D:\\Music\\'
        songs = os.listdir(music_dir)
        if songs:
            os.startfile(os.path.join(music_dir, songs[0]))
            self.speak("Playing music")
            self.log_command("play music")
        else:
            self.speak("No music files found in the directory.")

    def tell_time(self):
        str_time = datetime.datetime.now().strftime("%H:%M:%S")
        self.speak(f"The time is {str_time}")
        self.log_command("time")

    def ai_response(self, query):
        try:
            os.environ["GROQ_API_KEY"] = "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"  
            client = Client(api_key=os.getenv("GROQ_API_KEY"))
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                    "role": "user",
                    "content": query
                    },
                ],
                temperature=1,
                max_tokens=1024,
                top_p=1,
                stream=True,
                stop=None,
            )

            
            response_text = ""
            for chunk in completion:
                response_text += chunk.choices[0].delta.content or ""

            if response_text:
                print(response_text)
                #self.speak(response_text)
                self.log_command(query)
            else:
                self.speak("I received no meaningful response. Please try again.")
        except Exception as e:
            print(f"An error occurred: {e}")
            self.speak("I encountered an error while processing your request. Please try again later.")



    def search_google(self, query):
        self.speak("Searching Google...")
        query = query.split("search")
        search = query[1]
        search = search.replace(" ","")
       
        webbrowser.open(f"https://www.google.com/search?q={''.join(search)}")
        self.log_command(f"search {query}")
        
    def search_youtube(self,query):
        query = query.split("for")
        search= query[1]
        search=search.replace(" ","+")
        webbrowser.open(f"https://www.youtube.com/results?search_query={''.join(search)}")
        
    def search_file_command(self,query):
        self.speak("Please tell me the name of the file you want to search.")
        # file_name = self.take_command().strip()
        # file_name = file_name.replace("dot",'.')
        # file_name=file_name.replace(" ","")
        file_name = input("Enter File Name >> ")
        if file_name and file_name != "none":
            self.speak(f"Searching for the file named {file_name} in the D drive.")
            fo.search_and_open_file("D:\\", file_name)
        else:
            self.speak("Enter Proper File Name")
            
    def delete_file(self,query):
        self.speak("Please tell me the name of the file you want to search.")
        # file_name = self.take_command().strip()
        # file_name = file_name.replace("dot",'.')
        # file_name=file_name.replace(" ","")
        file_name = input("Enter File Name >> ")
        if file_name and file_name != "none":
            self.speak(f"Searching for the file named {file_name} in the D drive.")
            fo.search_and_delet_file("D:\\", file_name)
        else:
            self.speak("Enter Proper File Name")
            
    def open_folder(self,query):
        self.speak("Tell me the name of folder to open")
        folder_name=input("Enter Folder Name >> ")
        if folder_name and folder_name!="none":
            self.speak(f"Searching for {folder_name} folder")
            fo.search_and_open_foldr(folder_name)
        else:
            self.speak("Enter Proper Folder Name")
            
            
    def handle_open_application(self, query):
        app_name = query.replace("open application ", "").strip()
        if app_name:
            open_application(app_name)
        else:
            self.speak("Please specify the application name.")
            
    def close_application(self,query):
        app_name_list = query.split(" ")
        app_name ="".join(app_name_list[1])
        self.speak(f"closing {app_name}")
        close_application(app_name)
                
    def search_music(self,query):
        self.speak("Please Tell the name of Music To Search ")
        music_name = self.take_command().strip
        music_name = music_name.replace(" ","+")
        webbrowser.open(f"https://music.youtube.com/search?q={''.join(music_name)}")

    def sleep(self):
        self.speak("Going to sleep. Say 'drashti' to wake me up.")
        self.sleep_mode = True

    def wake_up(self, query):
        if "drishti" in query:
            self.speak("I am awake. How can I assist you?")
            self.sleep_mode = False

    def answer_name(self, query):
        if "what is your name" in query:
            self.speak("My name is Drashti. How can I help you?")
            self.log_command(query)

    def additional_commands(self, query):
        if query in self.additional_commands_dict:
            response = self.additional_commands_dict[query]
            self.speak(response)
            self.log_command(query)

    def math_operations(self, query):
        try:
            if "add" in query or "plus" in query:
                numbers = [int(word) for word in query.split() if word.isdigit()]
                result = sum(numbers)
                self.speak(f"The result is {result}")
            elif "subtract" in query or "minus" in query:
                numbers = [int(word) for word in query.split() if word.isdigit()]
                result = numbers[0] - numbers[1]
                self.speak(f"The result is {result}")
            elif "multiply" in query or "times" in query:
                numbers = [int(word) for word in query.split() if word.isdigit()]
                result = numbers[0] * numbers[1]
                self.speak(f"The result is {result}")
            elif "divide" in query:
                numbers = [int(word) for word in query.split() if word.isdigit()]
                result = numbers[0] / numbers[1]
                self.speak(f"The result is {result}")
            self.log_command(query)
        except Exception:
            self.speak("I encountered an error while performing the operation.")

    def quit(self,query):
        self.speak("Goodbye! Have a great day Sir!")
        exit()

    def shutdown(self):
        os.system("taskkill /f /im *")
        os.system("shutdown /s /t 1")        
    def run(self):
        self.greet()
        command_map = {
            "go to sleep": self.sleep,
            "quit": self.quit,
            "exit": self.quit,
            "wikipedia": self.search_wikipedia,
            "play music": self.play_music,
            "time": self.tell_time,
            "search file": self.search_file_command,
            "delete file":self.delete_file,
            "open folder":self.open_folder,
            "search music":self.search_music,
            "what is your name": self.answer_name,
            "open application": self.handle_open_application,
            "close":self.close_application
            
        }

        while True:
            query = self.take_command()
            if self.sleep_mode:
                self.wake_up(query)
                continue

            executed = False
            for command, action in command_map.items():
                if command in query:
                    if command == "go to sleep":
                        action() 
                    else:
                        action(query)  
                    executed = True
                    break

            if not executed:
                if "open" in query:
                    
                    site_name = query.replace("open", "").strip()
                    if site_name:
                        self.open_website(site_name)
                    else:
                        self.speak("Please specify the website name.")
                elif "video" in query:
                    self.search_youtube(query)
                elif "search" in query:
                    self.search_google(query)
                elif "weather" in query:
                    city = query.split("weather of ")
                    self.get_weather(city[1])
                elif 'news' in query:
                    self.fetch_news()
                elif 'remember' in query:
                    self.handle_context(query)
                elif 'quit' in query:
                    self.quit()
                elif query in self.additional_commands_dict:
                    self.additional_commands(query)
                elif any(keyword in query for keyword in ["add", "subtract", "multiply", "divide"]):
                    self.math_operations(query)
                elif any(keyword in query for keyword in ["give me", "write", "make", "generate" ,"what" ,"who","how","when","where","convert"]):
                    self.ai_response(query)
                elif 'shutdown' in query:
                    self.shutdown()

if __name__ == "__main__":
    assistant = Jarvis()
    assistant.run() 