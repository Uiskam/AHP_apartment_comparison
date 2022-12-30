import PySimpleGUI as sg
import GUI.layouts.flat_data_manual_input as manual_input


def list_difference(list0, list1):
    return [item for item in list0 if item not in list1]


def add_spaces(string, length):
    while len(string) < length:
        string += '            '
    return string


def get_longest_string_length(list_of_strings):
    longest_string_length = 0
    for string in list_of_strings:
        if len(string) > longest_string_length:
            longest_string_length = len(string)
    return longest_string_length


def replace_(string):
    return string.replace('_', ' ')


def get_preferences_priority(preference_group, nb):
    if preference_group == 'all_preferences':
        active_preferences = manual_input.all_preferences
    elif preference_group == 'location':
        active_preferences = manual_input.location
    elif preference_group == 'standard':
        active_preferences = manual_input.standard
    else:
        raise ValueError('Invalid preference group')

    max_feature_length = get_longest_string_length(active_preferences)

    def record_compare_preferences(feature0, feature1):
        slider_position_value = [sg.Push(), sg.Text("features are considered equal",
                                                    key=f'{feature0}-{feature1}-slider-header'), sg.Push()]
        if preference_group == 'location':
            tmp = 7
        else:
            tmp = 3
        record = [sg.Text(f'{replace_(feature0)}', size=(max_feature_length - tmp, 1)),
                  sg.Slider(range=(-8, 8), resolution=1, orientation='h', size=(25, 20), default_value=0,
                            enable_events=True, disable_number_display=True,
                            key=f'{feature0}-{feature1}-slider'),
                  sg.Text(f'{replace_(feature1)}')]
        return slider_position_value, record

    header_text = ''
    if preference_group == 'all_preferences':
        header_text = 'All preferences priorities'
    elif preference_group == 'location':
        header_text = 'Location preferences priorities'
    elif preference_group == 'standard':
        header_text = 'Standard preferences priorities'

    header = [sg.Push(), sg.Text(text=header_text, font=("Arial Black", 12)), sg.Push()]
    footer = [sg.Push(), sg.Button('Previous', key=f'-prev{nb}-'), sg.Button('Next', key=f'-next{nb}-')]
    if nb == 0:
        footer = [sg.Push(), sg.Button('Next', key=f'-next{nb}-')]

    layout = [header]
    for i in range(len(active_preferences)):
        for j in range(i + 1, len(active_preferences)):
            slider_description, record_ = record_compare_preferences(active_preferences[i], active_preferences[j])
            layout.append(slider_description)
            layout.append(record_)

    layout.append(footer)
    return layout
