import bs4
import constants
import pprint
import json
import sys
import re

import xpath_soup
from factored import is_useful_paragraph, extract_from_para, tokenize

LOOKFOR = {'houselords', 'housecommons'}

class Extractor(object):
    def run(self, parser, file_annotation):
        records = []

        for chamber_flag in LOOKFOR:
            found = parser.find_all(chamber_flag)
            
            for container in found:
                date = self.get_date(container)
                paragraphs = container.find_all('p')
                useful = filter(is_useful_paragraph, paragraphs)

                for paragraph in useful:
                    pair = extract_from_para(paragraph)
                    datum = {
                        'source_file': file_annotation,
                        'container_id': self.identify(container),
                        'paragraph_id': self.identify(paragraph),
                        'member_name': pair[0],
                        'member_contribution': tokenize(pair[1]),
                        'chamber': chamber_flag,
                        'date': date
                    }
                    records.append(datum)
        return records

    def identify(self, element):
        xpath = xpath_soup.xpath_soup(element)
        return re.sub(r'^/html/body', '', xpath, count=1)

    def get_date(self, container):
        dates = [x for x in container.children if x.name == 'date']

        if not dates:
            raise Exception("failed to find date in chamber container")

        if not len(dates) == 1:
            raise Exception("should be only one date", dates)

        # Need to strip to take care of some stupid bits.
        iso_string = dates[0]['format'].strip()

        if not re.match(r'^\d{4}-\d{2}-\d{2}$', iso_string):
            raise Exception("date did not validate", iso_string)

        return iso_string

    def run_on_file(self, input_path):
        with open(input_path, 'r') as f:
            bs = bs4.BeautifulSoup(f, constants.DESIRED_BEAUTIFULSOUP_PARSER)

        return self.run(bs, file_annotation=input_path)

if __name__ == '__main__':
    obj = Extractor()
    result = obj.run_on_file('data/hansard-indented.xml')
    json.dump(result, sys.stdout, indent=4)
