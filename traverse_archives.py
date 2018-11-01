import bs4
import constants
import os
import sys
import random
from extract_with_chamber_annotation import Extractor
import pprint
import multiprocessing
from csv_transformer import transform_csv
import csv
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)8s - %(name)s - %(message)s"
)
        
extractor = Extractor()

input_dir = sys.argv[1]
paths = os.listdir(input_dir)
random.shuffle(paths)

FIELDNAMES = [
    'sentence_index',
    'content',
    'member_name',
    'date',
    'chamber',
    'paragraph_id',
    'container_id',
    'source_file'
]

def process_one_path(path):
    logging.info("processing path %s", path)

    full_path = os.path.join(input_dir, path)
    filename, extension = os.path.splitext(path)
    output_path = os.path.join(input_dir, filename + ".csv")

    with open(full_path, 'r') as fr:
        result = extractor.run(
            bs4.BeautifulSoup(fr, constants.DESIRED_BEAUTIFULSOUP_PARSER),
            file_annotation=path
        )

    transformed = transform_csv(result)

    with open(output_path, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(transformed)
    
    return True

def on_error(e):
    logging.error(e)

def on_complete(result):
    logging.info("completed")

cpu_count = multiprocessing.cpu_count()

logging.info("using pool of %d processes", cpu_count)

with multiprocessing.Pool(processes=cpu_count) as pool:
    results = []

    for path in paths:
        r = pool.apply_async(
            process_one_path,
            [path],
            callback=on_complete,
            error_callback=on_error
        )
        results.append(r)

    for r in results:
        r.wait()
        
