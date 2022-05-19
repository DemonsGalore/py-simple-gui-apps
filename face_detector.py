import PySimpleGUI as sg
import cv2

layout = [
    [sg.Image(key = '-IMAGE-')],
    [sg.Text('People in picture: 0', key = '-TEXT-', expand_x = True, justification = 'center')]
]

window = sg.Window('Face detector', layout)

# get video
video = cv2.VideoCapture(0)
# https://raw.githubusercontent.com/opencv/opencv/4.x/data/haarcascades/haarcascade_frontalface_default.xml
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

while True:
    event, values = window.read(timeout = 0)

    if event == sg.WIN_CLOSED:
        break

    _, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # face recognition is working better with gray images
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor = 1.3,
        minNeighbors = 7,
        minSize = (50, 50)
    )

    # draw the rectangles
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)

    # update the image
    imgbytes = cv2.imencode('.png', frame)[1].tobytes()
    window['-IMAGE-'].update(data = imgbytes)

    # update the text
    window['-TEXT-'].update(f'People in picture: {len(faces)}')

window.close()
