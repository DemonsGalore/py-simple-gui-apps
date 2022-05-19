import PySimpleGUI as sg
from bs4 import BeautifulSoup as bs
import requests

def get_weather_data(location):
    url = f'https://www.google.com/search?q=weather+{location}'
    session = requests.Session()
    session.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0'
    response = session.get(url)

    soup = bs(response.text, 'html.parser')
    location = soup.find('div', attrs = {'id': 'wob_loc'}).text
    time = soup.find('div', attrs = {'id': 'wob_dts'}).text
    weather = soup.find('span', attrs = {'id': 'wob_dc'}).text
    temp = soup.find('span', attrs = {'id': 'wob_tm'}).text
    return location, time, weather, temp

sg.theme('reddit')

image_column = sg.Column([[sg.Image(key = '-IMAGE-', background_color = '#FFFFFF')]])
info_column = sg.Column([
    [sg.Text('', key = '-LOCATION-', font = 'Calibri 30', background_color = '#FF0000', text_color = '#FFFFFF', pad = 0, visible = False)],
    [sg.Text('', key = '-TIME-', font = 'Calibri 16', background_color = '#000000', text_color = '#FFFFFF', pad = 0, visible = False)],
    [sg.Text('', key = '-TEMP-', font = 'Calibri 16', background_color = '#FFFFFF', text_color = '#000000', pad = (0, 10), visible = False, justification = 'center')],
])

layout = [
    [sg.Input(expand_x = True, key = '-INPUT-'), sg.Button('Enter', button_color = '#000000', border_width = 0)],
    [image_column, info_column]
]

window = sg.Window('Weather', layout)

while True:
    event, values = window.read()

    image = ''

    if event == sg.WIN_CLOSED:
        break

    if event == 'Enter':
        location, time, weather, temp = get_weather_data(values['-INPUT-'])
        window['-LOCATION-'].update(location, visible = True)
        window['-TIME-'].update(time, visible = True)
        window['-TEMP-'].update(f'{temp} \u2103 ({weather})', visible = True)

        # TODO: not working properly (different languages on requests, missing icons, ...)
        # https://gist.github.com/bzerangue/806934
        # sun
        if weather in ('Sun', 'Sunny', 'Clear', 'Clear with periodic cloudls', 'Mostly Sunny'):
            image = 'symbols/sun-96.png'

        # part sun
        if weather in ('Partly Sunny', 'Partly Cloudy', 'Stark bewölkt'):
            image = 'symbols/cloudy-day-96.png'

        # rain
        if weather in ('Showers', 'Scattered Showers'):
            image = 'symbols/rain-96.png'

        # thunder
        if weather in ('Scattered Thunderstorms'):
            image = 'symbols/cloud-lightning-96.png'

        # foggy
        if weather in (''):
            image = 'symbols/wind-96.png'

        # snow
        if weather in ('Rain and Snow', 'Light Snow'):
            image = 'symbols/snow-96.png'

        # storm
        if weather in ('Storm'):
            image = 'symbols/windsock-96.png'

        # cloudy
        if weather in ('Overcast', 'Mostly Cloudy'):
            image = 'symbols/cloudy-day-96.png'

        window['-IMAGE-'].update(image)

window.close()
