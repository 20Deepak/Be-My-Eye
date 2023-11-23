import cv2 as cv
import numpy as np
import pytesseract
import pyttsx3

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Load YOLO
net = cv.dnn.readNet("D:\\final project\\yolov3.weights", "D:\\final project\\yolov3.cfg")

classes = []
with open("coco.names", 'r') as f:
    classes = [line.strip() for line in f.readlines()]

layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

# Open a camera stream
cap = cv.VideoCapture(0)  # 0 represents the default camera, change it if you have multiple cameras

# Set the desired frame width and height
frame_width = 1280
frame_height = 720
cap.set(3, frame_width)
cap.set(4, frame_height)

# Set up Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'D:\\final project\\tesseract.exe'

while True:
    ret, frame = cap.read()
    if not ret:
        break
    blob = cv.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * frame_width)
                center_y = int(detection[1] * frame_height)
                w = int(detection[2] * frame_width)
                h = int(detection[3] * frame_height)
                x = int(center_x - w/2)
                y = int(center_y - h/2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
    indexes = cv.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    font = cv.FONT_HERSHEY_PLAIN
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            color = colors[i]
            cv.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv.putText(frame, label, (x, y + 30), font, 3, color, 3)

            # Read the detected label aloud
            engine.say(label)
            engine.runAndWait()
    cv.imshow("Real-Time Object Detection", frame)
    if cv.waitKey(1) & 0xFF == 27:  # Press the 'Esc' key to exit the real-time detection loop
        break
cap.release()
cv.destroyAllWindows()
