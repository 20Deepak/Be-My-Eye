import cv2
import pyttsx3
import time
from roboflow import Roboflow

# Initialize Roboflow
rf = Roboflow(api_key="pf7pHRuBUWLHc1PtGjg7")
project = rf.workspace().project("currency-note-detection-hmfqa")
model = project.version(1).model

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Open a connection to the camera (camera index 0 by default)
cap = cv2.VideoCapture(0)

# Initialize variables for tracking time
last_detection_time = time.time()
timeout_duration = 10  # seconds

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Perform inference on the frame
    prediction_result = model.predict(frame, confidence=40, overlap=30).json()

    # Extract the class label from the first prediction (assuming only one prediction is made)
    if prediction_result['predictions']:
        class_label = prediction_result['predictions'][0]['class']
        confidence = prediction_result['predictions'][0]['confidence']

        # Reset the timer since a detection occurred
        last_detection_time = time.time()

        # Speak the class label and confidence
        text_to_speak = f"Currency detected: {class_label}"
        engine.say(text_to_speak)
        engine.runAndWait()

        # Display the class label and confidence on the frame
        cv2.putText(frame, f"Class: {class_label} | Confidence: {confidence:.2f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    # Check if the timeout duration has passed
    if time.time() - last_detection_time > timeout_duration:
        print("No currency note detected for 10 seconds. Exiting...")
        break

    # Display the resulting frame
    cv2.imshow('currency', frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
