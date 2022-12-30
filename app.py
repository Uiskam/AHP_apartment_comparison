import PySimpleGUI as sg
import csv
import GUI.layouts.source_data_input as source_data_input
import GUI.layouts.flat_comparison as flat_comparison
import GUI.layouts.flat_data_manual_input as manual_input
import GUI.layouts.data_confirmation as data_confirmation
import GUI.layouts.data_processing as data_processing
import GUI.layouts.results as results
from GUI.layout_structure import LayoutStructure
import numpy as np
import sys


def read_data(filename):
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


def get_app_layouts():
    data = read_data(sys.argv[1])
    flat_features = manual_input.flat_features
    layout_idx = 0
    app_layouts = [[sg.Column(source_data_input.get_source_data_input(layout_idx), key=f'-{layout_idx}-')]]
    app_layouts = [[]]
    #layout_idx += 1
    for flat_feature in flat_features:
        visibility = False
        if flat_features.index(flat_feature) == 0:
            visibility = True
        app_layouts[0].append(
            sg.Column(flat_comparison.get_flat_comparison(flat_feature, data, layout_idx), visible=visibility,
                      key=f'-{layout_idx}-'))
        layout_idx += 1
    app_layouts[0].append(
        sg.Column(data_confirmation.get_data_confirmation(layout_idx), visible=False, key=f'-{layout_idx}-'))
    layout_idx += 1
    app_layouts[0].append(sg.Column(data_processing.get_data_processing(), visible=False, key=f'-{layout_idx}-'))
    layout_idx += 1
    app_layouts[0].append(sg.Column(results.get_results(), visible=False, key=f'-{layout_idx}-'))
    return app_layouts


def create_data_container(flats_quantity):
    flats = {}
    flat_features = manual_input.flat_features
    for feature in flat_features:
        flats[feature] = np.ones([flats_quantity, flats_quantity], dtype=float)
    return flats


def start():
    active_layout_structure = LayoutStructure.SOURCE_DATA_INPUT
    app_layouts = get_app_layouts()
    window = sg.Window('Flats comparator v1.0', app_layouts)
    while True:
        event, values = window.read()
        if event in (None, 'Exit', '-results_exit-'):
            break
        elif event == f'-next{active_layout_structure.value}-':
            window[f'-{active_layout_structure.value}-'].update(visible=False)
            active_layout_structure = active_layout_structure.next()
            window[f'-{active_layout_structure.value}-'].update(visible=True)
        elif event == f'-prev{active_layout_structure.value}-':
            window[f'-{active_layout_structure.value}-'].update(visible=False)
            active_layout_structure = active_layout_structure.previous()
            window[f'-{active_layout_structure.value}-'].update(visible=True)

        print(event, values)
