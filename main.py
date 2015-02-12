import math

features = []

def is_number(s):

    if s is None:
        return False

    try:
        float(s)
        return True

    except ValueError:
        return False

def read_features(file_in):
    with open(file_in) as f:
        for line in f:
            if line[-1] == '\n':
                line = line[0:-1]
                line = line.strip(' ')

            features.append(line)

def read_data(file_in):
    """ Read in file and split at commas
        Map values to features using dictionary comprehension

    Args:
        file_in: File input
    """
    feature_list = []

    with open(file_in) as f:
        for line in f:
            line = line[0:-1]
            line = line.strip(' ')
            entry = line.split(',')

            continuous_list = []
            categorical_list = []

            feature_map = {features[i]: entry[i] for i, n in enumerate(entry)}
            for f in feature_map:
                feature_map[f] = feature_map[f].strip(' ')
                if feature_map[f] == '?':
                    feature_map[f] = None

            feature_list.append(feature_map)
            data_list = feature_list

    return data_list

def median(lst):
    lst = sorted(lst)

    if len(lst) < 1:
            return None
    if len(lst) %2 == 1:
            return lst[((len(lst)+1)/2)-1]
    if len(lst) %2 == 0:
            return float(sum(lst[(len(lst)/2)-1:(len(lst)/2)+1]))/2.0

def continuousReport(file_data):
    """ Generate continuous report
    """
    print "" + file_data.__str__()
    report = {}
    feature_data = []
    not_missing = []

    for f in features:
        feature_data = [x[f] for x in file_data if is_number(x[f])]
        temp = [x for x in feature_data if x is not None]

        if len(feature_data) != 0:

            for x in temp:
                not_missing.append(int(x))

            report[f] = {}

            count = len(feature_data)
            #print "" + count.__str__()
            missing_counter = count - len(not_missing)
            #print "" + missing_counter.__str__()
            miss_percent = missing_counter/count * 100
            #print "" + miss_percent.__str__()
            min_value = min(not_missing)

            max_value = max(not_missing)

            # Quart One & Two
            not_missing.sort()
            n = len(not_missing)
            quart1 = n * (25/100)
            quart3 = n * (75/100)

            # Mean
            #print not_missing
            mean = sum(not_missing)/len(not_missing)

            # Median
            median_value = median(not_missing)

            # Standard Deviation
            temp = 0

            for z in not_missing:
                """
                not_missing is a list, when you do for z in not_missing z is the value not the key
                """
                temp += (z - mean) ** 2

            std_dev = math.sqrt(temp)

            # Get cardinal values
            card_values = {}
            for v in not_missing:
                card_values[v] = card_values.get(v, 0) + 1



def categoricalReport(file_data):
    """ Generate categorical report
    """

    report = {}

    #print "" + file_data.__str__()
    for f in features:
        feature_data = [x[f] for x in file_data if is_number(x[f])]
        not_missing = [x for x in feature_data if x is not None]

        if len(feature_data) != 0:
            report[f] = {}

            count = len(feature_data)
            missing_counter = count - len(not_missing)
            miss_percent = missing_counter/count * 100

            # Cardinal values
            card_values = {}
            for v in not_missing:
                card_values[v] = card_values.get(v, 0) + 1

            # First Mode
            mode1_holder = first_mode(not_missing)
            mode1 = mode1_holder[0]
            mode1_count = mode1_holder[1]
            mode1_percent = (count * 100) / mode1_count

            # Second Mode
            mode2_holder = second_mode(not_missing)
            mode2 = mode2_holder[0]
            mode2_count = mode2_holder[1]
            mode2_percent = (count * 100) / mode2_count

def first_mode(list):
    d = {}
    results = []

    # Count values
    for i in list:
        try:
            d[i] += 1
        except(KeyError):
            d[i] = 1

    # Find max
    keys = d.keys()
    maximum = 0

    for key in keys[1:]:
        if d[key] > maximum:
            maximum = d[key]

    for key in keys:
        if d[key] == maximum:
            results.append(key)
            results.append(maximum)

    return results

def second_mode(list):
    d = {}
    results = []

    # Count values
    for i in list:
        try:
            d[i] += 1
        except(KeyError):
            d[i] = 1

    # Find max
    keys = d.keys()
    maximum = 0

    for key in keys[1:]:
        if d[key] > maximum:
            maximum = d[key]

    # Find second highest
    second_highest = 0

    for key in keys[1:]:
        if d[key] < maximum:
            for k in keys:
                if d[key] > d[k]:
                    second_highest = d[key]

    for key in keys:
        if d[key] == second_highest:
            results.append(key)
            results.append(second_highest)

    return results

if __name__ == '__main__':
    read_features("Data\Featurenames.txt")
    data = read_data("Data\DataSet.txt")
    continuousReport(data)
    categoricalReport(data)