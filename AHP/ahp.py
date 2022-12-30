from AHP.PCMatrix import PCMatrix


def conver_to_pcmatrix(m):
    return PCMatrix(m)


def ahp(data):
    data = {}

    subs = {
        "location": ['availability_of_shops', 'commute_to_university', 'proximity_to_city_center'],
        "standard": ['ambient_noise', 'decoration_level', 'insolation', 'security']
    }

    #sub_labels = ['proximity_to_city_center', 'availability_of_shops', 'commute_to_university', 'security', 'insolation', 'decoration_level', 'ambient_noise']
    labels = ['location', 'price', 'roommate_number', 'size_of_the_flat', 'size_of_the_room', 'standard']

    order = {k: i for i, k in enumerate(labels)}

    ranking = []
    n = len(data["price"])
    pc_matrix = {k: PCMatrix(v) for k, v in data.items()}
    weights = {k: v.priority_vector for k, v in pc_matrix.items()}

    for a in range(n):
        final_rank = 0
        for key, value in weights:
            if key in labels:
                if key == "location" or key == "standard":
                    sub_rank = 0
                    for i, sub in enumerate(subs[key]):
                        sub_rank += value[i] * weights[sub][a]
                    final_rank += sub_rank * weights["all"][order[key]]
                else:
                    final_rank += value[a] * weights["all"][order[key]]
        ranking.append(final_rank)

    return ranking
