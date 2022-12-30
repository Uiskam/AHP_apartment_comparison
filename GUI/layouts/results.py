import PySimpleGUI as sg
import csv
from math import inf


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
        return rgb(255 * (1 - color), 255 * color, 0)


def get_mocked_results(flats_quantity):
    # reads the data from the csv file named resources/mock_results.csv and returns it
    data = []
    max_ranking = 1000 * flats_quantity
    for i in range(flats_quantity):
        data.append([i, max_ranking])
        max_ranking -= 1000
    return data


def get_results(flats_quantity):
    results = get_mocked_results(flats_quantity)

    def get_table_content():
        nonlocal results
        table_content = []
        max_ranking = -inf
        min_ranking = inf
        for _, ranking in results:
            ranking = int(ranking)
            if ranking > max_ranking:
                max_ranking = ranking
            if ranking < min_ranking:
                min_ranking = ranking

        for flat_no, ranking in results:
            table_content.append([sg.Push(),
                                  sg.Text(f'{flat_no}\t{ranking}',
                                          text_color=get_color_per_ranking(min_ranking, max_ranking, int(ranking))),
                                  sg.Push()])
        return table_content

    header = [sg.Push(), sg.Text('RESULTS', font=("Arial Black", 14)), sg.Push()]
    table_header = [sg.Push(), sg.Text('Flat no\tranking', font=("Arial Black", 10)), sg.Push()]

    footer = [sg.Push(), sg.Button('Exit', key='-results_exit-'), sg.Push()]
    layout = [
        header,
        table_header]
    layout.extend(get_table_content())
    layout.append(footer)
    return layout
