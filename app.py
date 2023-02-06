import PySimpleGUI as sg
import csv
import GUI.layouts.source_data_input as source_data_input
import GUI.layouts.flat_comparison as flat_comparison
import GUI.layouts.flat_data_manual_input as manual_input
import GUI.layouts.data_confirmation as data_confirmation
import GUI.layouts.data_processing as data_processing
import GUI.layouts.preferences_priority as preferences_priority
import GUI.layouts.results as results
from GUI.layout_structure import LayoutStructure
import numpy as np
import sys
from AHP.ahp import ahp


def read_config(filename):
    try:
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            data = list(reader)
        number_of_experts = data[1:2]
        number_of_experts = int(number_of_experts[0][0])
        ranking_method = data[3:]
        ranking_method = ranking_method[0][0]
        if ranking_method != 'evm' and ranking_method != 'gmm':
            raise ValueError(f'Invalid ranking method: {ranking_method} valid values: evm, gmm')
        return number_of_experts, ranking_method

    except FileNotFoundError:
        return []


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


def get_app_layouts(data, number_of_experts):
    def get_one_expert_layout(initial_idx):
        nonlocal data
        flat_features = manual_input.flat_features
        layout_idx = initial_idx
        app_layouts = []
        initial_visibility = True
        if layout_idx != 0:
            initial_visibility = False
        app_layouts.append(
            sg.Column(preferences_priority.get_preferences_priority('location', layout_idx), visible=initial_visibility,
                      key=f'-{layout_idx}-'))
        layout_idx += 1
        app_layouts.append(
            sg.Column(preferences_priority.get_preferences_priority('standard', layout_idx), visible=False,
                      key=f'-{layout_idx}-'))
        layout_idx += 1
        app_layouts.append(
            sg.Column(preferences_priority.get_preferences_priority('all_preferences', layout_idx), visible=False,
                      scrollable=True,
                      key=f'-{layout_idx}-'))
        layout_idx += 1

        for flat_feature in flat_features:
            visibility = False
            if flat_features.index(flat_feature) == 0:
                visibility = False
            app_layouts.append(
                sg.Column(flat_comparison.get_flat_comparison(flat_feature, data, layout_idx), visible=visibility,
                          key=f'-{layout_idx}-'))
            layout_idx += 1

        return app_layouts, layout_idx

    layouts = [[]]
    idx_counter = 0
    for i in range(number_of_experts):
        new_layouts, idx_counter = get_one_expert_layout(idx_counter)
        for new_layout in new_layouts:
            layouts[0].append(new_layout)

    print('data_confirmation', idx_counter)
    layouts[0].append(
        sg.Column(data_confirmation.get_data_confirmation(idx_counter), visible=False, key=f'-{idx_counter}-'))
    idx_counter += 1
    layouts[0].append(sg.Column(data_processing.get_data_processing(), visible=False, key=f'-{idx_counter}-'))
    idx_counter += 1
    layouts[0].append(sg.Column(results.get_results(len(data)), visible=False, key=f'-{idx_counter}-'))
    return layouts


def create_data_container(flats_quantity, number_of_experts):
    def create_expert_container():
        nonlocal flats_quantity
        flats = {}
        flat_features = manual_input.flat_features
        for feature in flat_features:
            # flats[feature] = np.ones([flats_quantity, flats_quantity], dtype=float)
            flats[feature] = [[1 for x in range(flats_quantity)] for y in range(flats_quantity)]
        flats['all'] = [[1 for x in range(len(manual_input.all_preferences))] for y in
                        range(len(manual_input.all_preferences))]
        flats['location'] = [[1 for x in range(len(manual_input.location))] for y in range(len(manual_input.location))]
        flats['standard'] = [[1 for x in range(len(manual_input.standard))] for y in range(len(manual_input.standard))]
        return flats

    data_container = []
    for i in range(number_of_experts):
        data_container.append(create_expert_container())
    return data_container


def calculate_preference(preference):
    tmp = abs(preference) + 1
    if preference < 1:
        return 1 / tmp
    else:
        return tmp


def get_flat_preference_description(preference, idx0, idx1):
    preference = int(preference)
    idx0 += 1
    idx1 += 1
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


def get_preferences_priority_description(preference, feature0, feature1):
    preference = int(preference)
    if preference == 1:
        return "features are considered equal"
    if 2 <= preference <= 3:
        return f"{feature0} is slightly more important than {feature1}"
    if 4 <= preference <= 5:
        return f"{feature0} is more important than flat {feature1}"
    if 6 <= preference <= 7:
        return f"{feature0} is much more important than flat {feature1}"
    if 8 <= preference <= 9:
        return f"{feature0} is significantly more important than flat {feature1}"


def get_preferences_group(feature0, feature1):
    location = manual_input.location
    standard = manual_input.standard
    all_preferences = manual_input.all_preferences
    if feature0 in all_preferences and feature1 in all_preferences:
        return ['all', all_preferences]
    if feature0 in location and feature1 in location:
        return ['location', location]
    if feature0 in standard and feature1 in standard:
        return ['standard', standard]
    raise ValueError('Invalid features combination')


# sort list of tuples by second element
def sort_list_of_tuples(list_of_tuples):
    list_of_tuples.sort(key=lambda x: x[1], reverse=True)
    return list_of_tuples


def calculate_results(flat_comparison_data, method):
    # import time
    # time.sleep(2)
    # print(flat_comparison_data.keys())
    ranking, inconsistency = ahp(flat_comparison_data, method)
    ranking = [(i, ranking[i]) for i in range(len(ranking))]
    ranking = sort_list_of_tuples(ranking)
    ranking = [(i, round(j, 2)) for i, j in ranking]
    return ranking, inconsistency


def get_next_layout_idx(cur_layout_idx):
    '''Zakładam, że dostaje cur_layout_idx PRZED inkrementacją'''
    nex_expert_idx = (cur_layout_idx + 1) // 14
    return cur_layout_idx + 1, nex_expert_idx


def get_prev_layout_idx(cur_layout_idx):
    '''Zakładam, że dostaje cur_layout_idx PRZED dekremtnacją'''
    nex_expert_idx = (cur_layout_idx - 1) // 14
    return cur_layout_idx - 1, nex_expert_idx


def start():
    number_of_experts, method = read_config(sys.argv[1])
    data = read_data(sys.argv[2])

    active_layout_idx = 0
    app_layouts = get_app_layouts(data, number_of_experts)
    flat_comparison_data = create_data_container(len(data), number_of_experts)

    window = sg.Window(f'Flats comparator v1.1 Expert{1}', app_layouts)
    flat_features = manual_input.flat_features
    flat_features_extended = flat_features + ['all', 'location', 'standard']
    cur_expert_idx = 0
    while True:
        event, values = window.read()
        if event in (None, 'Exit', '-results_exit-'):
            break
        elif event == f'-next{active_layout_idx}-':
            next_layout_idx, cur_expert_idx = get_next_layout_idx(active_layout_idx)

            if next_layout_idx < number_of_experts * 14:
                window.set_title(f'Flats comparator v1.1 Expert{cur_expert_idx + 1}')
            else:
                window.set_title(f'Flats comparator v1.1')
            window[f'-{active_layout_idx}-'].update(visible=False)
            active_layout_idx = next_layout_idx
            window[f'-{active_layout_idx}-'].update(visible=True)
        elif event == f'-prev{active_layout_idx}-':
            next_layout_idx, cur_expert_idx = get_prev_layout_idx(active_layout_idx)
            window.set_title(f'Flats comparator v1.1 Expert{cur_expert_idx + 1}')

            window[f'-{active_layout_idx}-'].update(visible=False)
            active_layout_idx = next_layout_idx
            window[f'-{active_layout_idx}-'].update(visible=True)

        event_details = event.split('-')
        print(event_details)

        if len(event_details) == 5 and event_details[1] in flat_features:
            event_details = event_details[1:]
            i = int(event_details[1])
            j = int(event_details[2])
            cur_preference = calculate_preference(values[event])
            flat_comparison_data[cur_expert_idx][event_details[0]][i][j] = 1 / cur_preference
            flat_comparison_data[cur_expert_idx][event_details[0]][j][i] = cur_preference
            if cur_preference >= 1:
                window[f'{event}-header'].update(get_flat_preference_description(cur_preference, j, i))
            else:
                window[f'{event}-header'].update(get_flat_preference_description(1 / cur_preference, i, j))
        elif len(event_details) == 4 and event_details[1] in flat_features_extended and event_details[
            2] in flat_features_extended:
            event_details = event_details[1:]
            cur_preference = calculate_preference(values[event])
            preference_group, preferences_list = get_preferences_group(event_details[0], event_details[1])
            i = preferences_list.index(event_details[0])
            j = preferences_list.index(event_details[1])
            flat_comparison_data[cur_expert_idx][preference_group][i][j] = 1 / cur_preference
            flat_comparison_data[cur_expert_idx][preference_group][j][i] = cur_preference
            event_details[0] = event_details[0].replace('_', ' ')
            event_details[1] = event_details[1].replace('_', ' ')
            if cur_preference >= 1:
                window[f'{event}-header'].update(
                    get_preferences_priority_description(cur_preference, event_details[1], event_details[0]))
            else:
                window[f'{event}-header'].update(
                    get_preferences_priority_description(1 / cur_preference, event_details[0], event_details[1]))

        elif event == '-confirmation_confirm-':
            next_layout_idx, cur_expert_idx = get_next_layout_idx(active_layout_idx)

            window.set_title(f'Flats comparator v1.1 Expert{cur_expert_idx + 1}')
            window[f'-{active_layout_idx}-'].update(visible=False)
            active_layout_idx = next_layout_idx
            window[f'-{active_layout_idx}-'].update(visible=True)

            ranking, inconsistencies = calculate_results(flat_comparison_data, method)

            for i in range(len(ranking)):
                window[f'-result{i}-'].update(f'{ranking[i][0] + 1}\t{ranking[i][1]}')
                if len(inconsistencies) != 0:
                    window[f'-inconsistency-header-'].update(visible=True)
                    window[f'-inconsistency-content-'].update(visible=True)
                    inconsistency_text = ''
                    for inconsistency in inconsistencies:
                        inconsistency_text += f'{inconsistency}\n'
                    window[f'-inconsistency-content-'].update(f'{inconsistency_text}')

            next_layout_idx, cur_expert_idx = get_next_layout_idx(active_layout_idx)

            window.set_title(f'Flats comparator v1.1 Expert{cur_expert_idx + 1}')
            window[f'-{active_layout_idx}-'].update(visible=False)
            active_layout_idx = next_layout_idx
            window[f'-{active_layout_idx}-'].update(visible=True)
        # print(event, values)
        # print all key in values dict each key in seperate line
        # print(*values, sep='\n')
