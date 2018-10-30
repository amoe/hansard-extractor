import validation
import bs4
import constants
import nltk
import pdb
import json

def istag(x):
    return isinstance(x, bs4.element.Tag)

def get_parser(text):
    return bs4.BeautifulSoup(text, constants.DESIRED_BEAUTIFULSOUP_PARSER)

def extract_from_para(p):
    # At this point because they've already been validated we know that
    # they have the correct structure.
    #
    # We use decode() to obtain a Unicode string with full markup.  Because
    # membercontributions have their own markup.
    member = p.find_all('member')[0].decode()
    membercontribution = p.find_all('membercontribution')[0].decode()

    return (member, membercontribution)


unflattenable_tags = set(['image'])

def get_strings(contribution):
    bs4 = get_parser(contribution)
    result = []

    for child in bs4.membercontribution.children:
        if istag(child):
            if child.name not in unflattenable_tags:
                result.extend(list(child.strings))
        else:
            result.append(child)

    return ' '.join(result)

def extract_sentences(contribution):
    flat_text = get_strings(contribution)
    return nltk.sent_tokenize(flat_text, language='english')

with open('data/hansard-indented.xml', 'r') as f:
    bs = get_parser(f)

validator = validation.Validator()

paragraphs = bs.find_all('p')
useful_paragraphs = []

for p in paragraphs:
    try:
        validator.validate_paragraph(p)
        useful_paragraphs.append(p)
    except validation.ValidationError:
        pass


pairs = []

for p in useful_paragraphs:
    pair = extract_from_para(p)
    pairs.append(pair)

data = []

for pair in pairs:
    sentences = extract_sentences(pair[1])
    datum = {
        'member': pair[0],
        'sentences': sentences
    }
    data.append(datum)


with open('foo.json', 'w') as f:
    json.dump(data, f, indent=4)
