import bs4
import pdb

class ValidationError(Exception):
    pass

def require(condition, desc):
    if not condition:
        raise ValidationError(desc)

def is_relevant_child(val):
    if isinstance(val, bs4.NavigableString):
        if val.strip():
            return True
        else:
            return False

    return True

def get_non_whitespace_contents(tag):
    return [val for val in tag.contents if is_relevant_child(val)]

class Validator(object):
    def validate(self, xml_text):
        bs = bs4.BeautifulSoup(xml_text, 'lxml')

        try:
            for paragraph in bs.find_all('p'):
                self.validate_paragraph(paragraph)
            return True
        except ValidationError as e:
            raise e


    def validate_paragraph(self, p):
        contents = get_non_whitespace_contents(p)

        require(len(contents) == 2, "must have two children")
        require(isinstance(contents[0], bs4.element.Tag), "first element must be tag")
        require(isinstance(contents[1], bs4.element.Tag), "second element must be tag")
        require(contents[0].name == 'member', "member first")
        require(contents[1].name == 'membercontribution', "membercontribution second")


obj = Validator()

def validate(xml_text):
    return obj.validate(xml_text)
