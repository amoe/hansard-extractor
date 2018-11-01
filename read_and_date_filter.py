# Listdir
# read csv rows
# if date is in range, immediately write to a csv
# all source files will be combined to a single csv

import os
import csv
import sys

input_dir = sys.argv[1]
output_path = sys.argv[2]

def date_in_range(row):
    date = row[3]
    # because dates are already 8601 we can compare them cheaply
    return (date > '1880-01-01') and (date < '1910-01-01')

with open(output_path, 'w') as fw:
    w = csv.writer(fw)
    for path in os.listdir(input_dir):
        full_path = os.path.join(input_dir, path)
        with open(full_path, 'r') as fr:
            r = csv.reader(fr)
            for row in r:
                if date_in_range(row):
                    w.writerow(row)
            
