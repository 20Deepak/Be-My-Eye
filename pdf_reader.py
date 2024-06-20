import PyPDF2
import tkinter as tk
from tkinter import filedialog
from tkinter.simpledialog import askinteger  # Import askinteger for getting user input
import pyttsx3
import speech_recognition as sr

def pdf_reader(pdf_file, page_number=None):
    try:
        pdf_document = PyPDF2.PdfReader(pdf_file)
        engine = pyttsx3.init()

        line_count = 0  # Initialize line count

        if page_number is not None:
            if 0 < page_number <= len(pdf_document.pages):
                page = pdf_document.pages[page_number - 1]
                page_text = page.extract_text()
                print(f"Page {page_number}:\n")
                lines = page_text.split('\n')
                for line in lines:
                    print(line)
                    speak_text(engine, line)
                    line_count += 1
                    if line_count % 10 == 0:
                        if not continue_reading(engine):
                            break
                speak_text(engine, "End of page.")
            else:
                print(f"Invalid page number. Please choose a page between 1 and {len(pdf_document.pages)}.")
        else:
            for page_number, page in enumerate(pdf_document.pages, start=1):
                page_text = page.extract_text()
                print(f"Page {page_number}:\n")
                lines = page_text.split('\n')
                for line in lines:
                    print(line)
                    speak_text(engine, line)
                    line_count += 1
                    if line_count % 10 == 0:
                        if not continue_reading(engine):
                            break
                speak_text(engine, "End of page.")
                line_count = 0  # Reset line count for a new page

    except Exception as e:
        print(f"An error occurred: {str(e)}")

def speak_text(engine, text):
    engine.say(text)
    engine.runAndWait()

def select_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        # Use askinteger to get the page number
        page_number = askinteger("Enter Page Number", "Enter the page number you want to read (or press Cancel to read all pages):", minvalue=1)
        pdf_reader(file_path, page_number)

def continue_reading(engine):
    speak_text(engine, "Do you want to continue reading? Say yes or no.")
    
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source, timeout=5)

    try:
        user_input = recognizer.recognize_google(audio).lower()
        print(f"User said: {user_input}")
        return user_input == 'yes'
    except sr.UnknownValueError:
        print("Speech Recognition could not understand audio.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
    
    return False

if __name__ == "__main__":
    select_file()
