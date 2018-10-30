import bs4
import constants

with open('data/hansard-indented.xml', 'r') as f:
    bs = bs4.BeautifulSoup(f, constants.DESIRED_BEAUTIFULSOUP_PARSER)


contributions = bs.find_all('membercontribution')

for x in contributions:
    x.decompose()

members = bs.find_all('member')

for x in members:
    x.decompose()

print(bs.prettify())
