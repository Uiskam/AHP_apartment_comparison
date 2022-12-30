import PySimpleGUI as sg


def get_source_data_input(nb):
    csv_column = [[sg.Text('Select a CSV file to load', key='-CSV_text-')],
                  [sg.Push(), sg.FileBrowse('Select File', file_types=(('CSV Files', '*.csv'),), key="-file-"),
                   sg.Push()]]
    or_column = [[sg.Text('Select data input method (if both fields are filled file will be used)')],
                 [sg.Text('OR')]]
    manual_column = [[sg.Text('Enter data manually, enter number of flats to compare (non negative integer):')],
                     [sg.InputText(key='-flats-number-')]]
    footer = [[sg.Button('Next', key=f'-next{nb}-')]]
    layout = [
        [sg.Column(csv_column)],
        [sg.Push(), sg.Column(footer)]
    ]
    return layout
