import PySimpleGUI as sg
import csv

flat_features = ['ambient_noise', 'availability_of_shops', 'commute_to_university', 'decoration_level', 'insolation',
                 'price', 'proximity_to_city_center', 'roommate_number', 'security', 'size_of_the_flat',
                 'size_of_the_room']
features_units = ['dB', 'scale 1-10', 'average time', 'scale 1-10', 'scale 1-10', 'per month', 'km',
                  'non negative integer', 'scale 1-10', 'm^2', 'm^2']


def replace_underscore(string):
    return string.replace('_', ' ')


def get_feature_description(feature):
    return replace_underscore(feature) + ' [' + features_units[flat_features.index(feature)] + ']:'


def generate_unit(unit):
    if unit == 'dB':
        return 'dB'
    elif unit == 'scale 1-10':
        return 'scale 1-10'
    elif unit == 'average time':
        return 'min'
    elif unit == 'per month':
        return 'PLN'
    elif unit == 'km':
        return 'km'
    elif unit == 'non negative integer':
        return 'non negative integer'
    elif unit == 'm^2':
        return 'm^2'


def validate_features_input(values):
    def float_parser(value):
        try:
            return float(value)
        except ValueError:
            return -100

    def non_negative_int_parser(value):
        try:
            return int(value)
        except ValueError:
            return -100

    def scale_parser(value):
        try:
            scale_value = int(value)
            if scale_value < 1 or scale_value > 10:
                return -100
            return scale_value
        except ValueError:
            return -100

    validators = {
        'dB': "float",
        'scale 1-10': "scale",
        'average time': "float",
        'per month': "float",
        'km': "float",
        'non negative integer': "non_negative_integer",
        'm^2': "float"
    }
    feature_units = list(zip(flat_features, features_units))

    for i in range(len(values)):
        feature, unit = feature_units[i]
        if validators[unit] == "float":
            if float_parser(values[i]) == -100:
                return [False,
                        f'Invalid value for {replace_underscore(feature)}: {values[i]} is expected to be a {validators[unit]}']
        elif validators[unit] == "scale":
            if scale_parser(values[i]) == -100:
                return [False,
                        f'Invalid value for {replace_underscore(feature)}: {values[i]} is expected to be a {validators[unit]}']
        elif validators[unit] == "non_negative_integer":
            if non_negative_int_parser(values[i]) == -100:
                return [False,
                        f'Invalid value for {replace_underscore(feature)}: {values[i]} is expected to be a {validators[unit]}']


def get_flat_data_input(flat_quantity=3):
    def get_flat_input_column(flat_number):
        flat_column = [[sg.Text(f'flat{flat_number}:')]]
        features_input = [[sg.Text(get_feature_description(feature)), sg.Push(),
                           sg.InputText(key=f'-{feature}{flat_features.index(feature)}-')]
                          for feature in flat_features]
        # add features_input elements to flat_column
        flat_column.extend(features_input)
        return flat_column

    flats_input_columns = [get_flat_input_column(flat_number) for flat_number in range(flat_quantity)]
    navigation_column = [[sg.Push(), sg.Button('Previous'), sg.Button('Next')]]
    layout = [[
        [sg.Column(get_flat_input_column(flat_number + 1)) for flat_number in range(flat_quantity)],
        navigation_column
    ]]
    return layout
