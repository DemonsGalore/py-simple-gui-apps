import PySimpleGUI as sg
from pathlib import Path

emojis = [
    'monkeys', ['🙈', '🙉', '🙊'],
    'faces', ['🤡', '🤬', '🤑', '😭', '🥸', '🥳', '🥰', '🤮', '🥺'],
    'other', ['❤️', '🌍', '🦠', '👽', '💩', '💀'],
    'animals', ['🐳', '🦎', '🐙']
]
emoji_events = emojis[1] + emojis[3] + emojis[5] + emojis[7]

menu_layout = [
    ['File', ['Open', 'Save', '---', 'Exit']],
    ['Tools', ['Word count']],
    ['Add', emojis]
]

sg.theme('GrayGrayGray')

layout = [
    [sg.Menu(menu_layout)],
    [sg.Text('Untitled', key = '-DOCNAME-')],
    [sg.Multiline(no_scrollbar=True, size=(40,30), key='-TEXTBOX-')]
]

window = sg.Window('Texteditor', layout)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    if event == 'Word count':
        full_text = values['-TEXTBOX-']
        separated_text = full_text.replace('\n', ' ').split(' ')
        clean_text = []

        # remove empty strings
        for element in separated_text:
            if len(element) > 0:
                clean_text.append(element)

        word_count = len(clean_text)
        char_count = len(''.join(clean_text))
        sg.popup(f'words: {word_count}\ncharacters: {char_count}')

    if event == 'Open':
        file_path = sg.popup_get_file('open', no_window = True)
        if file_path:
            file = Path(file_path)
            window['-TEXTBOX-'].update(file.read_text())
            window['-DOCNAME-'].update(file_path.split('/')[-1])

    if event == 'Save':
        file_path = sg.popup_get_file('Save as', no_window = True, save_as = True) + '.txt'
        file = Path(file_path)
        file.write_text(values['-TEXTBOX-'])
        window['-DOCNAME-'].update(file_path.split('/')[-1])

    if event in emoji_events:
        current_text = values['-TEXTBOX-']
        new_text = current_text + f' {event}'
        window['-TEXTBOX-'].update(new_text)

window.close()
