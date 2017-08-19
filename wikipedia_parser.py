import urllib
from urllib.parse import urlparse, urljoin
from urllib.request import urlopen
from bs4 import BeautifulSoup
import math
import time
import nltk
#from profile_parser import *

class wikipedia_parser():
    def __init__(self, url):
        self.url = url
        self.profile = ''

    def html_parse(self):
        try:
            self.html = urlopen(self.url).read()
        except urllib.error.URLError as e:
            print('Download error:', e.reason)
            self.html = None

        try:
            if self.html is not None or len(self.html) > 0:
                soup = BeautifulSoup(self.html, 'html.parser')
                desc = soup.find_all("div", "mw-parser-output")[0]
                #print(desc)
                #first_sentence = desc.find_all("p")[0]
                first_sentence = None
                for child in desc.children:
                    if child.name == 'p' and len(child.text) > 5:
                        first_sentence = child.text
                        break

                self.profile = first_sentence
                print('\t\t\t', self.profile)
            else:
                self.profile = ''
                print('\t\t\t', 'There is no profile')
        except:
            self.profile = ''
            print('\t\t\t', 'A connection attempt failed')

if __name__ == '__main__':
    links = ['https://en.wikipedia.org/wiki/Bader_Abdulrahman',
             'https://en.wikipedia.org/wiki/Abdullah_Ahmad_Badawi',
            'https://en.wikipedia.org/wiki/A.B._Original',
            'https://en.wikipedia.org/wiki/Esmeral_Tun%C3%A7luer',
            'https://en.wikipedia.org/wiki/Mert_Tun%C3%A7o',
            'https://en.wikipedia.org/wiki/Tunde_and_Wunmi_Obe',
            'https://en.wikipedia.org/wiki/T%C3%BCnde_Hand%C3%B3',
            'https://en.wikipedia.org/wiki/Shambhuprasad_Tundiya',
            'https://en.wikipedia.org/wiki/Carl_Tundo',
            'https://en.wikipedia.org/wiki/Max_Tundra',
            'https://en.wikipedia.org/wiki/Niels_Tune-Hansen',
            'https://en.wikipedia.org/wiki/Ben_Tune',
            'https://en.wikipedia.org/wiki/David_Tune',
            'https://en.wikipedia.org/wiki/Dire_Tune',
            'https://en.wikipedia.org/wiki/Tommy_Tune',
            'https://en.wikipedia.org/wiki/Lane_Turner',
            'https://en.wikipedia.org/wiki/Precision_Tunes',
            'https://en.wikipedia.org/wiki/Sara_Tunes',
            'https://en.wikipedia.org/wiki/Andr%C3%A9s_T%C3%BA%C3%B1ez',
            'https://en.wikipedia.org/wiki/Mateo_T%C3%BAnez',
            'https://en.wikipedia.org/wiki/Tung_Ngo',
            'https://en.wikipedia.org/wiki/Tung-Mow_Yan',
            ]

    for link in links:
        print(link)
        app1 = wikipedia_parser(link)
        app1.html_parse()
        #app2 = profile_parser(app1.profile)
        #app2.parse()
        #app2.get_full_names()
        #app2.get_category()
        #app2.get_birthday()



