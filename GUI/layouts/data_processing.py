import PySimpleGUI as sg


def get_data_processing():
    header = [[sg.Push(), sg.Text('Calculating results...', font=("Arial Black", 12)), sg.Push()]]
    layout = [[
        header,
    ]]
    return layout
