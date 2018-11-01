import bs4
import constants
import os
import sys
import random
from extract_with_chamber_annotation import Extractor
import pprint
from csv_transformer import transform_csv

extractor = Extractor()

input_dir = sys.argv[1]
paths = os.listdir(input_dir)
random.shuffle(paths)

for path in paths:
    full_path = os.path.join(input_dir, path)
    filename, extension = os.path.splitext(path)
    output_path = os.path.join(input_dir, filename + ".csv")
    result = extractor.run_on_file(full_path)
    transformed = transform_csv(result)
    pprint.pprint(transformed)

