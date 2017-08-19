import urllib
from urllib.parse import urlparse, urljoin
from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv
import math
import time
from wikipedia_parser import *
from profile_parser import *


class controller():
    def __init__(self, start_url):
        self.start_url = start_url
        self.links = []
        self.link_cnt = 0
        self.page_cnt = 0

    def total_scrap(self):
        print('Program Started!!!')

        while(self.start_url is not None):
            self.onepage_parsing()

        print('All process done successfully!!!')


    def onepage_parsing(self):
        self.page_cnt += 1
        print('\tPage\t'+ str(self.page_cnt) +'\t:\tparsing and downloading...')

        try:
            self.html = urlopen(self.start_url).read()
        except urllib.error.URLError as e:
            print('\tDownload error:', e.reason)
            self.html = None

        soup = BeautifulSoup(self.html, 'html.parser')
        tables = soup.find_all("div", "mw-category-group")
        links = []
        for table in tables:
            for link in table.find_all('li'):
                link = link.a['href']
                links.append(link)

        self.links.extend(links)
        self.link_cnt += len(links)

        soup = BeautifulSoup(self.html, 'html.parser')

        next_page = None
        for link in soup.find_all('a'):
            if link.string == 'next page':
                next_page = link['href']

        if next_page is not None:
            self.start_url = 'https://en.wikipedia.org' + next_page
        else:
            self.start_url = None

        if self.link_cnt % 50000 == 0 or self.start_url is None:
            print('\t\tSaving new 50K of data into csv...')
            file_name = 'result_' + str(math.floor(self.link_cnt/1000)) + 'K.csv'
            csv_file = open(file_name, 'w', encoding='utf-8', newline='')
            writer = csv.writer(csv_file, dialect='excel')
            headers = ['ID', 'First Name', 'Middle Name', 'Last Name', 'Date of Birth', 'Birthplace', 'Category', 'URL']
            writer.writerow(headers)

            index = 0
            for link in self.links:
                link = 'https://en.wikipedia.org' + link
                print('\t\t', link)
                wiki_parser = wikipedia_parser(link)
                wiki_parser.html_parse()
                pro_parser = profile_parser(wiki_parser.profile)
                if pro_parser.isProfile:
                    pro_parser.parse()

                index += 0
                row = [index,
                       pro_parser.first_name,
                       pro_parser.middle_name,
                       pro_parser.last_name,
                       pro_parser.birthday,
                       pro_parser.birthplace,
                       pro_parser.category,
                       link]
                writer.writerow(row)

            csv_file.close()
            self.links = []
            print('\t\tSaved Successfully')


        print('\t\t\t\t\tparsed successfully!!!')

if __name__ == '__main__':

    start_time = time.time()
    app = controller('https://en.wikipedia.org/wiki/Category:Living_people?')
    app.total_scrap()

    print('Elapsed time is ', str(time.time()-start_time))
