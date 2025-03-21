import cv2
import speech_recognition as sr
import pyttsx3
import webbrowser
import os
import subprocess
from datetime import datetime
import tkinter as tk
from PIL import Image, ImageTk

class VideoAvatar:
    def __init__(self, video_source="video.mp4"):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.geometry("+0+0")
        self.root.attributes('-topmost', True)
        self.root.configure(bg="black")

        self.cap = cv2.VideoCapture(video_source)
        if not self.cap.isOpened():
            print("Error: Unable to open video file!")
            self.root.destroy()
            return

        self.label = tk.Label(self.root, bg="black")
        self.label.pack()

        self.update_video()
        self.root.mainloop()

    def update_video(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.resize(frame, (150, 150))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = ImageTk.PhotoImage(Image.fromarray(frame))
            self.label.config(image=img)
            self.label.image = img
        else:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

        self.root.after(30, self.update_video)

    def close(self):
        self.cap.release()
        self.root.destroy()

def speak(text):
    """Convert text to speech without delay"""
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Set to male voice
    engine.setProperty('volume', 0.5)  # Lower the volume
    engine.setProperty('speed', 1.5)  # Lower the speed
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen for voice commands and execute instantly"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)  # Reduce background noise
        try:
            print("Listening...")
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=6)
            command = recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
        except sr.WaitTimeoutError:
            return None  # Skip if no input detected
        except sr.UnknownValueError:
            return None  # Ignore if speech is not understood
        except sr.RequestError:
            print("Could not connect to the recognition service.")
            return None

def execute_command(command):
    """Executes the recognized voice command"""
    if "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif "open chat gpt" in command:
        speak("Opening ChatGPT")
        webbrowser.open("https://chat.openai.com")

    elif "ask chat gpt for"  in command:
        query = command.replace("ask chatgpt for", "").strip()
        speak(f"Asking ChatGPT for {query}")
        webbrowser.open(f"https://chat.openai.com/?q={query}")

    elif "open lead code" in command:
        speak("Opening LeetCode")
        webbrowser.open("https://leetcode.com")

    elif "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    elif "open vscode" in command or "open visual studio code" in command or "open vs code" in command:
        speak("Opening Visual Studio Code")
        os.system("code")  # This works if VS Code is added to the system PATH

    elif "open facebook" in command:
        speak("Opening Facebook")
        webbrowser.open("https://www.facebook.com")
        
    elif "open instagram" in command:
        speak("Opening instagram")
        webbrowser.open("https://www.instagram.com")

    elif "open notepad" in command:
        speak("Opening Notepad")
        os.startfile("notepad.exe")

    elif "open calculator" in command:
        speak("Opening Calculator")
        os.startfile("calc.exe")

    elif "open command prompt" in command or "open cmd" in command:
        speak("Opening Command Prompt")
        os.system("start cmd")

    elif "open file explorer" in command:
        speak("Opening File Explorer")
        os.system("explorer")

    elif "shutdown computer" in command:
        speak("Shutting down the computer")
        os.system("shutdown /s /t 1")

    elif "restart computer" in command:
        speak("Restarting the computer")
        os.system("shutdown /r /t 1")

    elif "lock" in command:
        speak("Locking the computer")
        os.system("rundll32.exe user32.dll,LockWorkStation")

    elif "search for" in command:
        query = command.replace("search for", "").strip()
        speak(f"Searching Google for {query}")
        webbrowser.open(f"https://www.google.com/search?q={query}")

    elif "find video" in command:
        query = command.replace("find video", "").strip()
        speak(f"Searching YouTube for {query}")
        webbrowser.open(f"https://www.youtube.com/results?search_query={query}")

    elif "time" in command:
        speak(datetime.now().strftime("The time is %I:%M %p"))

    elif "date" in command:
        speak(datetime.now().strftime("Today's date is %A, %B %d, %Y"))

    elif "exit" in command or "turn off" in command or "power off" in command:
        speak("Goodbye Sir!")
        exit()
    else:
        speak("Sorry, I didn't understand the command.")

def working():
    """Continuously listens and executes commands with 'Jarvis' as trigger word"""
    while True:
        command = listen()
        if command and "jarvis" in command:
            command = command.replace("jarvis", "").strip()
            execute_command(command)

if __name__ == "__main__":
    from threading import Thread
    video_thread = Thread(target=VideoAvatar)
    video_thread.start()
    working()
