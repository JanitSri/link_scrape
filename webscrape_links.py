''' 
NAME: Janit Sriganeshaelankovan 
CREATED: July 15, 2018 - 03:29 (EDT)
GOAL: Web Scrape All links off Website 
ENVIRONMENT: Base 
LAST UPDATE: January 24, 2019 - 13:01 (EDT)
'''


import os
import requests 
from bs4 import BeautifulSoup as soup
import re
from urllib.parse import urlparse
import sys

os.getcwd()


social_media = ['facebook', 'WhatsApp', 'Youtube', 'Tumblr', 'Instagram','QQ', 
                'WeChat', 'QZone', 'Twitter', 'Google', 'Skype', 'Linkedin']
main_url = 'https://vigilantglobal.com/'
url_list = [main_url]
#len(url_list)
#len(set(url_list))


''' ACTUAL GETTING THE LINKS '''
def get_all_links(url):
    print(len(url_list))
    resp = requests.get(url)
    print(url)
    html = resp.text
    page_soup = soup(html, 'lxml')
    body = page_soup.body
    try:
        found_links = [link.get('href') for link in body.find_all('a')]
        return found_links
    except Exception as e:
        print(e)
        sys.exit(1)
    
        
''' HANDLING LOCAL LINKS '''
def handle_local(url):
    for x in get_all_links(url):
        if x:
            if x.startswith(main_url) and x not in url_list:
                url_list.append(x)
            else:
                x = x.rstrip('/')
                if x.startswith('/'):    
                    urls = ''.join([main_url, x])
                    if urls not in url_list:
                        url_list.append(urls)
                  
                    
''' CALLING THE FUNCTIONS '''
def main():
    for link in url_list:
        handle_local(link)
        
main()


''' FILTERING OUT THE FRENCH '''
def french_filter():
    match = re.compile('/fr/')
    filtered = [i for i in url_list if not match.search(i)]
    print(filtered)
#    print(len(filtered))
    return filtered
    

file = open('vigilantglobal_fr_filter.txt', 'w')
for links in french_filter():
    file.write("%s\n" % links)
file.close()


''' GETTING THE PARA TEXT '''
links_para = dict()
def getp():
    
    for links in french_filter():
        resp = requests.get(links)
        html = resp.text
        page_soup = soup(html, 'lxml')
        body = page_soup.body
        found_para = body.find_all('p')
        links_para[links] = found_para
        
    return links_para.items()   
    
getp()



''' WRITING THE LINKS TO A TXT '''
def write_txt():
   file = open('vigilantglobal_test.txt', 'w')
   for links in url_list:
       file.write("%s\n" % links)
   file.close()
   
write_txt()


''' WRITING THE LINKS AND PARA TO A TXT '''
def write_txt2():
    file = open('vigilantglobal_links_para.txt', 'w', encoding="utf-8")
    for key, value in links_para.items():
#        print(str(key) + str(value))
        file.write('*****' + str(key) + '*****' + '\n\n' + str([i.text for i in value]) + '\n\n\n\n') 
    file.close()
    
write_txt2()


# GET HOSTNAME
hostname = urlparse('https://vigilantglobal.com').hostname
hostname.rsplit('.', 1)[0]


# MATCHING URLS 
pattern_url = r'((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*'
match = re.search(pattern_url, '//www.facebook.com/VigilantGlobal/')
print("Match at index %s, %s" % (match.start(), match.end()))
print("Full match: %s" % (match.group(0)))

    
    
    
    
    
    
    
    
    
    
    
    
    