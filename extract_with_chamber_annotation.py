import bs4
import constants
import pprint
import json
import sys

from factored import is_useful_paragraph, extract_from_para, tokenize


with open('data/hansard-indented.xml', 'r') as f:
    bs = bs4.BeautifulSoup(f, constants.DESIRED_BEAUTIFULSOUP_PARSER)


lookfor = {'houselords', 'housecommons'}
records = []

for chamber_flag in lookfor:
    found = bs.find_all(chamber_flag)

    for container in found:
        paragraphs = container.find_all('p')
        useful = filter(is_useful_paragraph, paragraphs)
        
        for paragraph in useful:
            pair = extract_from_para(paragraph)
            datum = {
                'member_name': pair[0],
                'member_contribution': tokenize(pair[1]),
                'chamber': chamber_flag
            }
            records.append(datum)

json.dump(records, sys.stdout, indent=4)
