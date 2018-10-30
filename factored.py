import bs4
import validation
import constants
import nltk

unflattenable_tags = set(['image'])
validator = validation.Validator()

def get_parser(text):
    return bs4.BeautifulSoup(text, constants.DESIRED_BEAUTIFULSOUP_PARSER)

def is_useful_paragraph(p):
    try:
        validator.validate_paragraph(p)
        return True
    except validation.ValidationError:
        pass

def extract_from_para(p):
    # At this point because they've already been validated we know that
    # they have the correct structure.
    #
    # We use decode() to obtain a Unicode string with full markup.  Because
    # membercontributions have their own markup.
    member = p.find_all('member')[0].decode()
    membercontribution = p.find_all('membercontribution')[0].decode()

    return (member, membercontribution)


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

def tokenize(contribution):
    flat_text = get_strings(contribution)
    return nltk.sent_tokenize(flat_text, language='english')

def istag(x):
    return isinstance(x, bs4.element.Tag)
