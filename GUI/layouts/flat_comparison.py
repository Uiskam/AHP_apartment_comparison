import PySimpleGUI as sg
import GUI.layouts.flat_data_manual_input as manual_input


def get_flat_comparison(feature, flats):
    flat_features = manual_input.flat_features
    features_units = manual_input.features_units

    def record_compare_flats(flat1_idx, flat2_idx):
        nonlocal feature
        slider_position_value = [sg.Push(), sg.Text("flats are equal",
                                                    key=f'-{feature}{flat1_idx}{flat2_idx}_slider_header-'), sg.Push()]
        record = [sg.Text(f'flat{flat1_idx + 1}: {flats[flat1_idx][feature]}'),
                  sg.Slider(range=(-8, 8), resolution=1, orientation='h', size=(25, 20), default_value=0,
                            disable_number_display=True, key=f'-{feature}{flat1_idx}{flat2_idx}_slider-'),
                  sg.Text(f'{flats[flat2_idx][feature]} :flat{flat2_idx + 1}')]
        return slider_position_value, record

    header = [[sg.Push(),
               sg.Text(text=(feature.replace('_', ' ') + f' {features_units[flat_features.index(feature)]}'),
                       font=("Arial Black", 12)), sg.Push()]]
    footer = [sg.Push(), sg.Button('Previous', key=f'-{feature}_prev-'), sg.Button('Next', key=f'-{feature}_next-')]
    flat_quantity = len(flats)
    layout = [[
        [header],
        [record_compare_flats(flat1_idx, flat2_idx) for flat1_idx in range(flat_quantity)
         for flat2_idx in range(flat1_idx + 1, flat_quantity)],
        [footer]

    ]]

    return layout
