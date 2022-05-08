import PySimpleGUI as sg

layout = [
    [sg.Text('Text', enable_events = True, key = '-TEXT-'), sg.Spin(['item 1', 'item 2'])],
    [sg.Button('Button', key = '-BUTTON1-')],
    [sg.Input(key = '-INPUT-')],
    [sg.Text('Test'), sg.Button('Test Button', key = '-BUTTON2-')]
]

window = sg.Window('Coverter', layout)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    if event == '-BUTTON1-':
        # print()
        window['-TEXT-'].update(values['-INPUT-'])

    if event == '-BUTTON2-':
        print('test button pressed')

    if event == '-TEXT-':
        print('text was pressed')

window.close()
