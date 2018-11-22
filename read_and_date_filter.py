# Listdir
# read csv rows
# if date is in range, immediately write to a csv
# all source files will be combined to a single csv

import os
import csv
import sys
import fieldnames

input_dir = sys.argv[1]
output_path = sys.argv[2]

csv.field_size_limit(sys.maxsize)

TARGET_ROW_INDEX = 2



def date_in_range(row):
    date = row[TARGET_ROW_INDEX]
    # because dates are already 8601 we can compare them cheaply
    return (date > '1880-01-01') and (date < '1910-01-01')

with open(output_path, 'w') as fw:
    w = csv.writer(fw, quoting=csv.QUOTE_ALL)
    w.writerow(fieldnames.FIELDNAMES)
    for path in os.listdir(input_dir):
        print("reading", path)
        full_path = os.path.join(input_dir, path)
        with open(full_path, 'r') as fr:
            r = csv.reader(fr)
            for row in r:
                if date_in_range(row):
                    w.writerow(row)
            
