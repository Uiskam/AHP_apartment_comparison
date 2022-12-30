import PySimpleGUI as sg


def get_data_confirmation(nb):
    header = [sg.Push(), sg.Text('All preferences has been entered', font=("Arial Black", 12)), sg.Push()]

    footer = [sg.Push(), sg.Button('Previous', key=f'-prev{nb}-')]
    layout = [
        header,
        [sg.Push(), sg.Button('Confirm and calculate ranking', key='-confirmation_confirm-'), sg.Push()],
        footer
    ]
    return layout
