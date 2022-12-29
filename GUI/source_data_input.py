import PySimpleGUI as sg


def get_source_data_input():
    csv_column = [[sg.Text('Select a CSV file to load')],
                  [sg.FileBrowse('Select File', file_types=(('CSV Files', '*.csv'),), key="-file-")]]
    or_column = [[sg.Text('Select data input method (if both fields are filled file will be used)')],
                 [sg.Text('OR')]]
    manual_column = [[sg.Text('Enter data manually, enter number of flats to compare (non negative integer):')],
                     [sg.InputText(key='-flats-number-')]]
    navigation_column = [[sg.Button('Previous')], [sg.Button('Next')]]
    layout = [[
        [sg.Column(csv_column),
         # sg.Column(or_column),
         # sg.Column(manual_column)
         ],
        [sg.Push(), sg.Column(navigation_column)]
    ]]
    return layout
