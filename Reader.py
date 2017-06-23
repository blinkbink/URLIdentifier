import re
import csv

fh = open("dataset.csv", "r")
reader = csv.reader(fh, delimiter='+')

dataset = {}
no_of_items = {}
feature_set = {}

# For each sentence in dataset
for row in reader:
    no_of_items.setdefault(row[1],0)
    no_of_items[row[1]] += 1
    dataset.setdefault(row[1],{})
    split_data = re.split('[^a-zA-Z\']',row[0])
    # For every word in split data
    for i in split_data:
        # Removing stop words to a small extent by ignoring words with length less than 3
        if len(i) > 2:
            dataset[row[1]].setdefault(i.lower(), 0)
            dataset[row[1]][i.lower()] += 1
            feature_set.setdefault(i.lower(), {})
            feature_set[i.lower()].setdefault(row[1], 0)
            feature_set[i.lower()][row[1]] += 1