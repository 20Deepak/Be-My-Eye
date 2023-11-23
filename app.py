import tkinter as tk
from tkinter import PhotoImage
import speech_recognition as sr
import threading
import subprocess

# Creating Tkinter window
root = tk.Tk()
root.geometry("400x400")
root.title("Voice Control")

# Create voice command
def voice_command():
    # Initializing speech recognizer
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak something")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("Google Speech Recognition:", text)
        if text.lower() == "talk":
            show_ocr_screen()
        elif text.lower() == "read":
            show_text_screen()
        elif text.lower() == "walk":
            show_object_screen()
        elif text.lower() == "exit":
            root.quit()  # Exit the application
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

# Create home screen
def show_home_screen():
    mic_img = PhotoImage(file="D:\\final project\\mic.png")
    mic_img = mic_img.subsample(3, 3)
    canvas.create_image(200, 200, image=mic_img)
    canvas.bind("<Button-1>", click_microphone)

# Create OCR screen
def show_ocr_screen():
    subprocess.call(["python", "D:\\final project\\ocr.py"], cwd="D:\\final project")  
    print("Reading....")

# Create a text to speech screen
def show_text_screen():
    subprocess.call(["python", "pdf reader.py"], cwd="D:\\final project")  
    print("TTS....")

# Create a object screen
def show_object_screen():
    subprocess.call(["python", "object detection.py"], cwd="D:\\final project")  
    print("Object Detection....")

# Function to be called on clicking the microphone image
def click_microphone(event):
    t = threading.Thread(target=voice_command)
    t.start()

# Create a microphone image
mic_img = PhotoImage(file="D:\\final project\\mic.png")
mic_img = mic_img.subsample(3, 3)

# Put the microphone image on the window and bind it with the function to be called on clicking it
canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()
canvas.create_image(200, 200, image=mic_img)
canvas.bind("<Button-1>", click_microphone)

# Run the Tkinter main loop
root.mainloop()