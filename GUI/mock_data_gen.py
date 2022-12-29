import random
from GUI.layouts import flat_data_manual_input
import csv


def save_to_csv(data, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        for row in data:
            writer.writerow(row)


def generate_unit(unit, lower_bound, upper_bound):
    def generate_float(low, high):
        return round(random.uniform(low, high), 2)

    def generate_non_negative_integer(low, high):
        return random.randint(low, high)

    def generate_scale():
        return random.randint(1, 10)

    if unit == "float":
        return generate_float(lower_bound, upper_bound)
    elif unit == "non_negative_integer":
        return generate_non_negative_integer(lower_bound, upper_bound)
    elif unit == "scale":
        return generate_scale()
    else:
        raise ValueError(f'Invalid unit: {unit}')


def get_one_flat():
    features_bounds = {'ambient_noise': (10, 70),
                       'availability_of_shops': None,
                       'commute_to_university': (5, 120),
                       'decoration_level': None,
                       'insolation': None,
                       'price': (800, 1500),
                       'proximity_to_city_center': (0.5, 5),
                       'roommate_number': (0, 4),
                       'security': None,
                       'size_of_the_flat': (20, 90),
                       'size_of_the_room': (10, 30)}
    flat_data = []
    feature_units = dict(zip(flat_data_manual_input.flat_features, flat_data_manual_input.features_units))
    unit_values = flat_data_manual_input.units_values
    for feature, unit in feature_units.items():
        if features_bounds[feature] is None:
            flat_data.append(generate_unit(unit_values[unit], 1, 10))
        else:
            flat_data.append(generate_unit(unit_values[unit], features_bounds[feature][0], features_bounds[feature][1]))
    return flat_data


def generate_mock_results(flat_quantity):
    ranking = []
    for i in range(flat_quantity):
        ranking.append((i + 1, random.randint(1500, 2000)))
    ranking.sort(key=lambda x: x[1], reverse=True)
    return ranking


def generate_mock_data(flat_number=5):
    features = flat_data_manual_input.flat_features
    units = flat_data_manual_input.features_units
    feature_units = list(zip(features, units))
    save_to_csv(data=generate_mock_results(flat_number), filename='resources/mock_results.csv')
    with open('resources/mock_data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(features)
        for i in range(flat_number):
            flat_data = get_one_flat()
            writer.writerow(flat_data)

print("ASDASD")
#generate_mock_data()
