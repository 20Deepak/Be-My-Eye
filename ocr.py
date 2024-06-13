import cv2
import pytesseract
import pyttsx3
import time

# Set the path to your Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'D:/home/C3 PROJECT/file of ocr/tesseract.exe'

# Initialize the camera
camera = cv2.VideoCapture(0)

# Initialize the text-to-speech engine
engine = pyttsx3.init()

start_time = time.time()
while True:
    # Capture a frame from the camera
    _, frame = camera.read()

    # Convert the frame to grayscale (optional but can improve OCR accuracy)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Perform OCR on the grayscale frame
    detected_text = pytesseract.image_to_string(gray_frame)

    # Display the recognized text on the frame
    cv2.putText(frame, detected_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display the frame with recognized text
    cv2.imshow('Text Detection', frame)

    if detected_text.strip():  # Check if the detected text is not empty
        engine.say(detected_text)
        engine.runAndWait()
        start_time = time.time()  # Reset the timer

    elapsed_time = time.time() - start_time
    if elapsed_time > 10:  # Stop after 10 seconds of inactivity
        break

    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera
camera.release()

# Close all OpenCV windows
cv2.destroyAllWindows()
