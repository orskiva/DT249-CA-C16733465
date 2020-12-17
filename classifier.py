import requests
import csv

from utils import *
from constants import *

# keeps track of the total number of instances of each attribute, as well as the totals for l & g
from utilities import read_file, remove_attributes

TOTAL_VAL_COUNTS = {
    'totals': {'l': 0, 'g': 0},
    'Private': [0, 0],
    'Self-emp-not-inc': [0, 0],
    'Self-emp-inc': [0, 0],
    'Federal-gov': [0, 0],
    'Local-gov': [0, 0],
    'State-gov': [0, 0],
    'Without-pay': [0, 0],
    'Never-worked': [0, 0],
    'Married-civ-spouse': [0, 0],
    'Divorced': [0, 0],
    'Never-married': [0, 0],
    'Separated': [0, 0],
    'Widowed': [0, 0],
    'Married-spouse-absent': [0, 0],
    'Married-AF-spouse': [0, 0],
    'Tech-support': [0, 0],
    'Craft-repair': [0, 0],
    'Other-service': [0, 0],
    'Sales': [0, 0],
    'Exec-managerial': [0, 0],
    'Prof-specialty': [0, 0],
    'Handlers-cleaners': [0, 0],
    'Machine-op-inspct': [0, 0],
    'Adm-clerical': [0, 0],
    'Farming-fishing': [0, 0],
    'Transport-moving': [0, 0],
    'Priv-house-serv': [0, 0],
    'Protective-serv': [0, 0],
    'Armed-Forces': [0, 0],
    'Wife': [0, 0],
    'Own-child': [0, 0],
    'Husband': [0, 0],
    'Not-in-family': [0, 0],
    'Other-relative': [0, 0],
    'Unmarried': [0, 0],
    'White': [0, 0],
    'Asian-Pac-Islander': [0, 0],
    'Amer-Indian-Eskimo': [0, 0],
    'Other': [0, 0],
    'Black': [0, 0],
    'Male': [0, 0],
    'Female': [0, 0]
}


# converts "<=50k" and ">50k" into l & g
# removes unnecessary attributes at indexes 2,3,13
def transform_data(data):
    cleaned_dataset = []
    for record in data.split("\n"):
        if '?' in record:
            continue
        else:
            try:
                # split string into array fields
                # remove whitespace on attributes
                record = record.strip().split(",")
                record = [x.strip() for x in record]

                record = remove_attributes(record, [2, 3, 13])

                if record[-1] == '<=50K':
                    record[-1] = 'l'
                elif record[-1] == '>50K':
                    record[-1] = 'g'
                else:
                    raise ValueError("income is undefined")

                cleaned_dataset.append(record)

            except ValueError as val_err:
                print(f"Record {record[0]} rejected: {val_err}")
                continue

    return tuple(cleaned_dataset)


# For each attrib in the record, increase the corresponding dict. property
def count_val_quantity(dataset):
    for record in dataset:
        if record[-1] == 'l':
            TOTAL_VAL_COUNTS['totals']['l'] += 1
        elif record[-1] == 'g':
            TOTAL_VAL_COUNTS['totals']['g'] += 1

        for attribute in range(len(record)):
            key = record[attribute]
            if key in TOTAL_VAL_COUNTS:
                if record[-1] == 'l':
                    TOTAL_VAL_COUNTS[key][0] += 1
                elif record[-1] == 'g':
                    TOTAL_VAL_COUNTS[key][1] += 1


# converts attributes into their weighted averages
def weigh_records(dataset):
    for record in dataset:
        for attribute in range(len(record)):
            value = record[attribute]
            if value in TOTAL_VAL_COUNTS:
                if record[-1] == 'l':
                    record[attribute] = TOTAL_VAL_COUNTS[value][0] / TOTAL_VAL_COUNTS['totals']['l']
                else:
                    record[attribute] = TOTAL_VAL_COUNTS[value][1] / TOTAL_VAL_COUNTS['totals']['g']
            else:
                for i in range(len(record) - 1):
                    if record[i] not in TOTAL_VAL_COUNTS:
                        record[i] = float(record[i])
        continue


def create_classifier(training_dataset):
    """For each record:
    - Average the values for each attribute in a list of known greater results and, separately, a list of known lesser results.
    - The greater and lesser averages are then averaged against each other to compute midpoint values.
    - These will be used to compare each attribute in a record and assign it a status (greater or lesser).
    - Overall result is the bigger of the number of the greater / lesser status values.
    """
    l_attributes = [0] * 11
    g_attributes = [0] * 11
    l_count = 0
    g_count = 0
    classifier_mid_points = [0] * 11

    # Compute the totals for each factor
    for record in training_dataset:
        if record[-1] == 'l':
            l_count += 1
            for attribute in range(len(record[1:-1])):
                l_attributes[attribute] += record[attribute]

        elif record[-1] == 'g':
            g_count += 1
            for attribute in range(len(record[1:-1])):
                g_attributes[attribute] += record[attribute]

    # Compute the average values for each factor
    for attribute in range(len(l_attributes)):
        l_attributes[attribute] = l_attributes[attribute] / l_count
    for attribute in range(len(g_attributes)):
        g_attributes[attribute] = g_attributes[attribute] / g_count

    # Compute the midpoints - the average of the L & G factors in each case
    for attribute in range(len(classifier_mid_points)):
        classifier_mid_points[attribute] = (l_attributes[attribute] + g_attributes[attribute]) / 2

    print(f"Classifier values\n{'-' * 50}")
    for item in classifier_mid_points:
        print(f"{item:.4f}", end=", ")
    print("\n")

    return tuple(classifier_mid_points)


def test_classifier(testing_dataset, classifier_mid_points):
    false_count = 0
    true_count = 0
    total_count = 0

    temp_result_list = [''] * 12
    for record in testing_dataset:
        print(record)
        for attribute in range(len(record[:-1])):
            if record[attribute] > classifier_mid_points[attribute]:
                temp_result_list[attribute] = 'g'
            else:
                temp_result_list[attribute] = 'l'

        if temp_result_list.count('g') >= 6:
            temp_result_list[-1] = 'g'
        else:
            temp_result_list[-1] = 'l'

        print(temp_result_list, end=' ')

        total_count += 1
        if record[-1] == temp_result_list[-1]:
            true_count += 1
            print("CORRECT")
        else:
            false_count += 1
            print("FALSE")

    print(f"\nCORRECT: {true_count}, {true_count / total_count:.2%},  INCORRECT: {false_count}, "
          f"{false_count / total_count:.2%},  TOTAL COUNT: {total_count}")


def main():
    with open(FILE, 'w') as f:
        res = requests.get(DATA_URL)
        writer = csv.writer(f)
        for line in res.iter_lines():
            writer.writerow(line.decode('utf-8').split(','))

    FILE_CONTENT = read_file(FILE)

    cleaned_dataset = transform_data(FILE_CONTENT)

    count_val_quantity(cleaned_dataset)

    weigh_records(cleaned_dataset)

    training_dataset = cleaned_dataset[:int(len(cleaned_dataset) * PERCENT / 100)]
    test_dataset = cleaned_dataset[int(len(cleaned_dataset) * PERCENT / 100):]

    classifier_mid_points = create_classifier(training_dataset)
    test_classifier(test_dataset, classifier_mid_points)


if __name__ == "__main__":
    main()
