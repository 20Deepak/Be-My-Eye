import PyPDF2
import tkinter as tk
from tkinter import filedialog
import pyttsx3

def pdf_reader(pdf_file, page_number=None):
    try:
        pdf_document = PyPDF2.PdfReader(pdf_file)
        engine = pyttsx3.init()

        if page_number is not None:
            if 0 < page_number <= len(pdf_document.pages):
                page = pdf_document.pages[page_number - 1]
                page_text = page.extract_text()
                print(f"Page {page_number}:\n")
                print(page_text)
                speak_text(engine, page_text)
            else:
                print(f"Invalid page number. Please choose a page between 1 and {len(pdf_document.pages)}.")
        else:
            for page_number, page in enumerate(pdf_document.pages, start=1):
                page_text = page.extract_text()
                print(f"Page {page_number}:\n")
                print(page_text)
                speak_text(engine, page_text)

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
        page_number = input("Enter the page number you want to read (or press Enter to read all pages): ")

        try:
            page_number = int(page_number) if page_number.strip() else None
        except ValueError:
            page_number = None

        pdf_reader(file_path, page_number)

if __name__ == "__main__":
    select_file()
