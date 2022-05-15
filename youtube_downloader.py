import PySimpleGUI as sg
from io import BytesIO
from pytube import YouTube
from PIL import Image
from urllib import request

thumbnail_size = (480, 360)

def progress_check(stream, chunk, bytes_remaining):
    progress_amount = 100 - round(bytes_remaining / stream.filesize * 100)
    window['-PROGRESSBAR-'].update(progress_amount)

def on_complete(stream, file_path):
    window['-PROGRESSBAR-'].update(0)

def create_thumbnail(url):
    req = request.Request(url)
    response = request.urlopen(req)
    data = response.read()

    image = Image.open(BytesIO(data))
    bio = BytesIO()

    image.thumbnail(thumbnail_size, Image.ANTIALIAS)
    image.save(bio, format = 'PNG')

    window['-THUMBNAIL-'].update(data = bio.getvalue())


# default video link
video_link = 'https://www.youtube.com/watch?v=JbVXWcB5xAg'

sg.theme('Darkred1')

start_layout = [[sg.Input(video_link, key = '-INPUT-'), sg.Button('Submit')]]

info_tab = [
    [sg.Text('Title'), sg.Text('', key = '-TITLE-')],
    [sg.Text('Length:'), sg.Text('', key = '-LENGTH-')],
    [sg.Text('Views:'), sg.Text('', key = '-VIEWS-')],
    [sg.Text('Author:'), sg.Text('', key = '-AUTHOR-')],
    [
        sg.Text('Description:'),
        sg.Multiline('', key = '-DESCRIPTION-', size = (40, 20), no_scrollbar = True, disabled = True, expand_x = True)
    ],
    [sg.Push(), sg.Image('', key = '-THUMBNAIL-', size = thumbnail_size), sg.Push()]
]

download_tab = [
    [
        sg.Frame('Best Quality', [[
            sg.Button('Download', key = '-BEST-'),
            sg.Text('', key = '-BESTRES-'),
            sg.Text('', key = '-BESTSIZE-')
        ]])
    ],
    [
        sg.Frame('Worst Quality', [[
            sg.Button('Download', key = '-WORST-'),
            sg.Text('', key = '-WORSTRES-'),
            sg.Text('', key = '-WORSTSIZE-')
        ]])
    ],
    [
        sg.Frame('Audio', [[
            sg.Button('Download', key = '-AUDIO-'),
            sg.Text('', key = '-AUDIOSIZE-')
        ]])
    ],
    [sg.VPush()],
    [sg.Progress(100, size = (20, 20), expand_x = True, key = '-PROGRESSBAR-')]
]

layout = [
    [sg.TabGroup([[
        sg.Tab('Info', info_tab),
        sg.Tab('Download', download_tab)
    ]])]
]

window = sg.Window('YouTube Downloader', start_layout)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    if event == 'Submit':
        video_object = YouTube(values['-INPUT-'], on_progress_callback = progress_check, on_complete_callback = on_complete)
        window.close()

        # video info
        window = sg.Window('YouTube Downloader', layout, finalize = True)
        window['-TITLE-'].update(video_object.title)
        window['-LENGTH-'].update(f'{round(video_object.length / 60, 2)} minutes')
        window['-VIEWS-'].update(video_object.views)
        window['-AUTHOR-'].update(video_object.author)
        window['-DESCRIPTION-'].update(video_object.description)
        create_thumbnail(video_object.thumbnail_url)

        # download
        window['-BESTSIZE-'].update(f'{round(video_object.streams.get_highest_resolution().filesize / (1024 * 1024), 1)} MB')
        window['-BESTRES-'].update(video_object.streams.get_highest_resolution().resolution)

        window['-WORSTSIZE-'].update(f'{round(video_object.streams.get_lowest_resolution().filesize / (1024 * 1024), 1)} MB')
        window['-WORSTRES-'].update(video_object.streams.get_lowest_resolution().resolution)

        window['-AUDIOSIZE-'].update(f'{round(video_object.streams.get_audio_only().filesize / (1024 * 1024), 1)} MB')


    if event == '-BEST-':
        video_object.streams.get_highest_resolution().download()
    if event == '-WORST-':
        video_object.streams.get_lowest_resolution().download()
    if event == '-AUDIO-':
        video_object.streams.get_audio_only().download()

window.close()
