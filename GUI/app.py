import PySimpleGUI as sg
import GUI.flat_data_manual_input as manual_input
import csv

def generate_mock_data():
    features = manual_input.flat_features
    units = manual_input.features_units
    feature_units = list(zip(features, units))
    with open('resources/mock_data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(features)
        for i in range(5):
            row = []
            for feature in features:
                row.append(1)
            writer.writerow(row)

def read_csv(filename):
    try:
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            data = list(reader)
        return data
    except FileNotFoundError:
        return []


def start():
    layout = layouts.get_flat_data_input()
    window = sg.Window('Data Source Selection', layout)
    while True:
        event, values = window.read()
        if event in (None, 'Exit'):
            break
        print(event, values)
