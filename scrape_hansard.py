import re
import bs4

# http://www.hansard-archive.parliament.uk/



# http://www.hansard-archive.parliament.uk/Parliamentary_Debates_Vol_1_(1803)_to_Vol_41_(Feb_1820)/S1V0001P0.zip


#javascript:__doPostBack('ctl00$HistoricalHansardContentPlaceHolder$VolumeGrid$ctl14$ctl01','')

#javascript:__doPostBack('ctl00$HistoricalHansardContentPlaceHolder$VolumeGrid$ctl14$ctl02','')

import requests

url = "http://www.hansard-archive.parliament.uk/Parliamentary_Debates_Vol_1_(1803)_to_Vol_41_(Feb_1820)"

control_string = 'ctl00$HistoricalHansardContentPlaceHolder$VolumeGrid$ctl14$ctl02'

post_data = {
    '__EVENTTARGET': control_string,
    '__EVENTARGUMENT': ''
}


# r = requests.post(url, data=post_data)
# print(r.text)


r = requests.get(url)
bs = bs4.BeautifulSoup(r.text, 'lxml')


def is_js_link(element):
    if element.name == 'a' and element['href'].startswith('javascript:'):
        return True
    
    return False

js_links = bs.find_all(is_js_link)
control_strings = []

for link in js_links:
    href_target = link['href']
    result = re.search(r"'([^']+)'", href_target)
    control_strings.append(result.group(1))

print(control_strings)

# def find_input(id_):
#     result = bs.find_all(name='input', attrs={'id': id_})
#     return result[0]


# view_state = find_input("__VIEWSTATE").get('value')
# view_state_generator = find_input("__VIEWSTATEGENERATOR").get('value')
# event_validation = find_input("__EVENTVALIDATION").get('value')


# post_data['__VIEWSTATEGENERATOR'] = view_state_generator
# post_data['__EVENTVALIDATION'] = event_validation
# post_data['__VIEWSTATE'] = view_state

# print(post_data)
# r2 = requests.post(url, post_data)
# print(r2.text)

