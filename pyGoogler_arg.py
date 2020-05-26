#VERSION 0.1
#UNSTABLE, MESSY
#OUTPUTS [queryInput].csv in working folder


from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from googlesearch import search
import csv
import string
import re
import sys
import os
import time

i = 1
result_list = []

def scrapeTitle(url):
    try:
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = Request(url,headers=hdr)
        page = urlopen(req, timeout = 10)
        soup = BeautifulSoup(page.read().decode('utf-8', 'ignore'), "html.parser")
        return soup.title.text
    except Exception as error:
        return 'ERROR:' + str(error);
        pass  

print('Using argument as source file for query string')
with open(sys.argv[1], 'r') as stringSource:
    lines = []
    for line in stringSource:
        queryInput = re.sub(r'[\n\r\t]*', '', line)
        print("Fetching results for string " + queryInput)
        csvFilename = queryInput.replace(' ', '_') + '.csv'
        while True:
            try:
                for url in search(queryInput,        # The query you want to run
#                           tld = 'com',  # The top level domain
#                           lang = 'en',  # The language
#                           start = 0,    # First result to retrieve
#                           stop = 20,  # Last result to retrieve
                            num = 10,     # Number of results per page
                            pause = 5.0,  # Lapse between HTTP requests
                           ):
                    result = []
                    title = re.sub(r'[\n\r\t]*', '', scrapeTitle(url))
                    if 'ERROR:' in title:
                        errorMsg = title
                        title = ""
                        result = ([url, title, i, errorMsg])
                    else:
                        result = ([url, title, i])
            
                    result_list.append(result)
                    data = [result]
                    wr = open('RESULTS/' + csvFilename, 'a', newline ='')
                    with wr:
                        write = csv.writer(wr)
                        write.writerows(data)
                    print(result)
                    print(" ")
                    i += 1
#                    break
            except Exception as error:
                if "Too Many Requests" in str(error):
                    print('Too many requests, sleeping for 5 minutes...')
                    time.sleep(300.0)
                    pass
