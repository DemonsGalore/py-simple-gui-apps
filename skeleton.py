import PySimpleGUI as sg

layout = [
    []
]

window = sg.Window('Skeleton', layout)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

window.close()
