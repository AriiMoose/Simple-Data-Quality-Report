import numpy as np
import csv
import statistics
from collections import Counter

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

    with open(file_in, 'r') as f:
        for line in f:
            line = line[0:-1]
            line = line.strip(' ')
            entry = line.split(',')

            continuous_list = []
            categorical_list = []

            feature_map = {features[i]: entry[i] for i, n in enumerate(entry)}
            for f in feature_map:
                feature_map[f] = feature_map[f].strip(' ')
                if feature_map[f] == '?' or feature_map[f] == 0:
                    feature_map[f] = None

            feature_list.append(feature_map)
            data_list = feature_list

    return data_list

def continuousReport(file_data):
    """ Generate continuous report
    """
    report = {}
    feature_data = []
    not_missing = []

    csvfile = open('c11347281CONT.csv', 'w', newline = "")
    fieldnames = ['FEATURENAME', 'Count', 'Miss %', 'Cardinality',
                  'Min', '1st Quart', 'Mean', 'Median',
                  '3rd Quart', 'Max', 'Standard Deviation']
    contwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
    contwriter_header = csv.writer(csvfile, delimiter=",")
    contwriter_header.writerow(fieldnames)

    for f in features:
        feature_data = [x[f] for x in file_data if is_number(x[f]) or x[f] is None]
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
            n = np.array(not_missing)
            quart1 = np.percentile(n, 25)
            quart3 = np.percentile(n, 75)

            # Mean
            #print not_missing
            mean = sum(not_missing)/len(not_missing)

            # Median
            median_value = statistics.median(not_missing)

            # Standard Deviation
            std_dev = statistics.stdev(not_missing)

            # Get cardinal values
            card_values = len(set(not_missing))

            contwriter.writerow({'FEATURENAME': f, 'Count': count, 'Miss %': miss_percent, 'Cardinality': card_values,
                                 'Min': min_value, '1st Quart': quart1, 'Mean': mean, 'Median': median_value,
                                 '3rd Quart': quart3, 'Max': max_value, 'Standard Deviation': std_dev})

def categoricalReport(file_data):
    """ Generate categorical report
    """

    report = {}

    csvfile = open('c11347281CAT.csv', 'w')
    fieldnames = ['FEATURENAME', 'Count', 'Missing %',
                  'Cardinality', 'Mode', 'Mode Count',
                  'Mode %', '2nd Mode', '2nd Mode Count', '2nd Mode %']
    catwriter_header = csv.writer(csvfile, delimiter=",")
    catwriter_header.writerow(fieldnames)
    catwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
    iterfeatures = iter(features)
    next(iterfeatures)

    for f in iterfeatures:
        feature_data = [x[f] for x in file_data if not is_number(x[f])]
        not_missing = [x for x in feature_data if x is not None]

        if len(feature_data) != 0:
            report[f] = {}

            count = len(feature_data)
            missing_counter = count - len(not_missing)
            miss_percent = missing_counter/count * 100

            # Cardinal values
            card_values = len(set(not_missing))

            # First Mode
            temp_list = Counter(not_missing)
            mode1_temp = temp_list.most_common(1)
            mode1_holder = mode1_temp[0]
            mode1 = mode1_holder[0]
            mode1_count = temp_list.most_common().__len__()
            mode1_percent = (count * 100) / mode1_count

            # Second Mode
            temp_list2 = Counter(not_missing)
            mode2_temp = temp_list2.most_common(2)
            mode2_holder= mode2_temp[0]
            mode2 = mode1_holder[0]
            mode2_count = temp_list2.most_common().__len__()
            mode2_percent = (count * 100) / mode2_count

            catwriter.writerow({'FEATURENAME': f, 'Count': count, 'Missing %': miss_percent,
                                'Cardinality': card_values, 'Mode': mode1, 'Mode Count': mode1_count,
                                'Mode %': mode1_percent, '2nd Mode': mode2, '2nd Mode Count':mode2_count, '2nd Mode %': mode2_percent})

if __name__ == '__main__':
    read_features("./Data/Featurenames.txt")
    data = read_data("./Data/DataSet.txt")
    continuousReport(data)
    categoricalReport(data)
