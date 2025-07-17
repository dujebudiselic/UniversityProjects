import sys
import urllib.request
import re
from urllib.parse import urlparse

entry = sys.argv
url = entry[1]

try:
    stranica = urllib.request.urlopen(url)
    mybytes = stranica.read()
    mystr = mybytes.decode('utf8')
    print(mystr)
except Exception as e:
    print('Error opening URL:', e)

print('Links:')
links = re.findall(r'href="(http[s]?://[^"]+)"', mystr)
unique_links = set(links)
for link in unique_links:
    print(link)
print()

hosts = set()
host_count = {}
for link in links:
    host = urlparse(link).netloc
    hosts.add(host)
    if host in host_count:
        host_count[host] = host_count[host] + 1
    else:
        host_count[host] = 1

print('Hosts list: ', hosts)
for host, count in host_count.items():
    print(f"{host}: {count}")
print()

emails = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', mystr)
unique_emails = set(emails)
if unique_emails:
    print('Emails:')
    for email in unique_emails:
        print(email)
else:
    print('Emails: -')
print()

img_links = re.findall(r'<img\s+[^>]*src="([^"]+)"', mystr)
count_img = len(img_links)
print('Picture count: ', count_img)

