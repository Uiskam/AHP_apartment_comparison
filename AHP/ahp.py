from AHP.PCMatrix import PCMatrix
from scipy.stats.mstats import gmean



def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

def ahp(data, method):

    group_method="am"

    subs = {
        "location": ['availability_of_shops', 'commute_to_university', 'proximity_to_city_center'],
        "standard": ['ambient_noise', 'decoration_level', 'insolation', 'security']
    }


    labels = ['location', 'price', 'roommate_number', 'size_of_the_flat', 'size_of_the_room', 'standard']

    order = {k: i for i, k in enumerate(labels)}

    rankings = [[] for i in range(len(data))]
    n = len(data[0]["price"])
    pc_matrixs = [{k: PCMatrix(v, method) for k, v in expert.items()} for expert in data]

    weights = [{k: v.priority_vector for k, v in expert.items()} for expert in pc_matrixs]

    errors = [[k for k, v in expert.items() if not v.is_consistent()] for expert in pc_matrixs]

    for i in range(len(pc_matrixs)):
        for a in range(n):
            final_rank = 0
            for key, value in weights[i].items():
                if key in labels:
                    if key == "location" or key == "standard":
                        sub_rank = 0
                        for b, sub in enumerate(subs[key]):
                            sub_rank += value[b] * weights[i][sub][a]
                        final_rank += sub_rank * weights[i]["all"][order[key]]
                    else:
                        final_rank += value[a] * weights[i]["all"][order[key]]
            rankings[i].append(final_rank)

    ranking=[]
    if group_method == "am":
        ranking = [mean(row) for row in [[x[i] for x in rankings] for i in range(len(rankings[0]))]]
    elif group_method == "gmm":
        ranking = [gmean(row) for row in [[x[i] for x in rankings] for i in range(len(rankings[0]))]]
    return ranking,errors
