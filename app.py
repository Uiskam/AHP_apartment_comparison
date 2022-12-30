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


def get_app_layouts(data):
    flat_features = manual_input.flat_features
    layout_idx = 0
    app_layouts = [[]]
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
    app_layouts[0].append(sg.Column(results.get_results(len(data)), visible=False, key=f'-{layout_idx}-'))
    return app_layouts


def create_data_container(flats_quantity):
    flats = {}
    flat_features = manual_input.flat_features
    for feature in flat_features:
        flats[feature] = np.ones([flats_quantity, flats_quantity], dtype=float)
    return flats


def calculate_preference(preference):
    tmp = abs(preference) + 1
    if preference < 1:
        return 1 / tmp
    else:
        return tmp


def get_preference_description(preference, idx0, idx1):
    preference = int(preference)
    if preference == 1:
        return "flats are equal"
    if 2 <= preference <= 3:
        return f"flat {idx0} is slightly better than flat {idx1}"
    if 4 <= preference <= 5:
        return f"flat {idx0} is better than flat {idx1}"
    if 6 <= preference <= 7:
        return f"flat {idx0} is much better than flat {idx1}"
    if 8 <= preference <= 9:
        return f"flat {idx0} is significantly better than flat {idx1}"


def calculate_results(flat_comparison_data):
    import time
    time.sleep(2)


def start():
    data = read_data(sys.argv[1])
    active_layout_structure = LayoutStructure.FLAT_COMPARISON_AMBIENT_NOISE
    app_layouts = get_app_layouts(data)
    flat_comparison_data = create_data_container(len(data))

    window = sg.Window('Flats comparator v1.0', app_layouts)
    flat_features = manual_input.flat_features
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
        event_details = event.split('-')
        if len(event_details) == 4 and event_details[0] in flat_features:
            i = int(event_details[1])
            j = int(event_details[2])
            cur_preference = calculate_preference(values[event])
            flat_comparison_data[event_details[0]][i][j] = cur_preference
            flat_comparison_data[event_details[0]][j][i] = 1 / cur_preference
            if cur_preference >= 1:
                window[f'{event}-header'].update(get_preference_description(cur_preference, j, i))
            else:
                window[f'{event}-header'].update(get_preference_description(1 / cur_preference, i, j))

        if event == '-confirmation_confirm-':
            window[f'-{active_layout_structure.value}-'].update(visible=False)
            active_layout_structure = active_layout_structure.next()
            window[f'-{active_layout_structure.value}-'].update(visible=True)
            calculate_results(flat_comparison_data)
            window[f'-{active_layout_structure.value}-'].update(visible=False)
            active_layout_structure = active_layout_structure.next()
            window[f'-{active_layout_structure.value}-'].update(visible=True)
        print(event, values)
