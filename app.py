import PySimpleGUI as sg
import csv
import GUI.layouts.source_data_input as source_data_input
import GUI.layouts.flat_comparison as flat_comparison
import GUI.layouts.flat_data_manual_input as manual_input
import GUI.layouts.data_confirmation as data_confirmation
import GUI.layouts.data_processing as data_processing
import GUI.layouts.results as results


def read_csv(filename):
    try:
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            data = list(reader)
        data = data[1:]
        parsed_data = []
        flat_features = manual_input.flat_features
        for flat_data in data:
            parsed_data.append({})
            if len(flat_data) != len(flat_features):
                raise ValueError('Invalid data format')

            for i in range(len(flat_data)):
                parsed_data[data.index(flat_data)][flat_features[i]] = flat_data[i]

        return parsed_data
    except FileNotFoundError:
        return []


def start():
    # layout = source_data_input.get_source_data_input()
    mock_data = read_csv('resources/mock_data.csv')
    print(mock_data)
    # return
    # layout = flat_comparison.get_flat_comparison('decoration_level', mock_data)
    # layout = data_confirmation.get_data_confirmation()
    #    layout = data_processing.get_data_processing()
    layout = results.get_results()
    window = sg.Window('Flats comparator v1.0', layout)
    while True:
        event, values = window.read()
        if event in (None, 'Exit'):
            break
        print(event, values)
