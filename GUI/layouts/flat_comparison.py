import PySimpleGUI as sg
import GUI.layouts.flat_data_manual_input as manual_input


def get_flat_comparison(feature, flats, nb):
    flat_features = manual_input.flat_features
    features_units = manual_input.features_units

    def record_compare_flats(flat1_idx, flat2_idx):
        nonlocal feature
        tmp1 = '  '
        if (flats[flat1_idx][feature]) == '10':
            tmp1 = ''

        slider_position_value = [sg.Push(), sg.Text("flats are equal",
                                                    key=f'-{feature}{flat1_idx}{flat2_idx}_slider_header-'), sg.Push()]
        record = [sg.Text(f'flat{flat1_idx + 1}: {flats[flat1_idx][feature]}{tmp1}'),
                  sg.Slider(range=(-8, 8), resolution=1, orientation='h', size=(25, 20), default_value=0,
                            enable_events=True, disable_number_display=True,
                            key=f'-{feature}_{flat1_idx}_{flat2_idx}_slider-'),
                  sg.Text(f'{flats[flat2_idx][feature]} :flat{flat2_idx + 1}')]
        return slider_position_value, record

    header = [sg.Push(),
              sg.Text(text=(feature.replace('_', ' ') + f' {features_units[flat_features.index(feature)]}'),
                      font=("Arial Black", 12)), sg.Push()]
    footer = [sg.Push(), sg.Button('Previous', key=f'-{feature}_prev-'), sg.Button('Next', key=f'-{feature}_next-')]
    footer = [sg.Push(), sg.Button('Previous', key=f'-prev{nb}-'), sg.Button('Next', key=f'-next{nb}-')]
    if nb == 0:
        footer = [sg.Push(), sg.Button('Next', key=f'-next{nb}-')]
    flat_quantity = len(flats)

    layout = [header]
    for flat1_idx_ in range(flat_quantity):
        for flat2_idx_ in range(flat1_idx_ + 1, flat_quantity):
            slider_description, record_ = record_compare_flats(flat1_idx_, flat2_idx_)
            layout.append(slider_description)
            layout.append(record_)

    layout.append(footer)
    return layout
