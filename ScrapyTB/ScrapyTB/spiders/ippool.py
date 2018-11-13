import random
import re
import requests

url = 'http://proxy.httpdaili.com/apinew.asp?text=true&noinfo=true&sl=10&ddbh=gs921302'
get_url = requests.get(url).text
re_url = re.findall(r'[\d]+.[\d]+.[\d]+.[\d]+:[\d]+', get_url)
print(re_url[1])


# IPPOOL=[
#
# ]

