import PySimpleGUI as sg
import csv


def rgb(red, green, blue):
    red = min(int(red), 255) if red > 0 else 0
    blue = min(int(blue), 255) if blue > 0 else 0
    green = min(int(green), 255) if green > 0 else 0
    return '#%02x%02x%02x' % (red, green, blue)


def get_color_per_ranking(min_ranking, max_ranking, cur_ranking):
    # returns a color depending on the ranking
    # the color is determined by the formula: (cur_ranking - min_ranking) / (max_ranking - min_ranking)
    # the color is then converted to rgb and returned
    if min_ranking == max_ranking:
        return rgb(0, 0, 0)
    else:
        color = (cur_ranking - min_ranking) / (max_ranking - min_ranking)
        return rgb(255 * color, 255 * (1 - color), 0)


def get_mocked_results():
    # reads the data from the csv file named resources/mock_results.csv and returns it
    with open('resources/mock_results.csv', 'r') as file:
        reader = csv.reader(file)
        data = list(reader)
    return data


def get_results(results=None):
    if results is None:
        results = get_mocked_results()
    header = [[sg.Push(), sg.Text('RESULTS', font=("Arial Black", 12), text_color=rgb(125, 0, 125)), sg.Push()]]
    footer = [[sg.Push(), sg.Button('Exit', key='-results_exit-'), sg.Push()]]
    layout = [[
        header,
        footer
    ]]
    return layout
