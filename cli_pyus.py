from __future__ import print_function, unicode_literals
import sys
import json
import requests
import pyshorteners
from PyInquirer import prompt
from colorama import init
init(strip=not sys.stdout.isatty())  # strip colors if stdout is redirected
from termcolor import cprint
from pyfiglet import figlet_format

# Handling user response
class UrlShortener(object):

    def __init__(self, shortenersource, url):
        self.shortener = pyshorteners.Shortener()
        self.shortenersource = shortenersource
        self.url = url

    # Method to shorten url
    def get_shorten_url(self):

        try:
            response = requests.get(self.url)
            shorter = ShortenerType(self.url)

            if response.status_code != 404:
                switcher = {
                    'TinyURL': shorter.tinyUrl,
                    'Chilp.it': shorter.chilpit,
                    'Da.gd': shorter.dagd
                }
                func = switcher.get(self.shortenersource, lambda: "Invalid shortener! Please try again.")
                return func()
        except:
                return "Invalid URL! Please try again."
    


class ShortenerType(object):
    def __init__(self, url):
        self.shortener = pyshorteners.Shortener()
        self.url = url

        # tinyUrl shortener
    def tinyUrl(self):
        return self.shortener.tinyurl.short(self.url)

    # Chilp.it shortener
    def chilpit(self):
        return self.shortener.chilpit.short(self.url)

    # Da.gd shortener
    def dagd(self):
        return self.shortener.dagd.short(self.url)



if __name__ == '__main__':

    # Welcome message
    cprint(figlet_format('PyUS', font='slant'))
    print("Welcome to PyUS!\n")

    # Question and fetch user response
    question = json.loads(open('question.json').read())
    response = prompt(question)

    # Assign user response to variables
    user_response_shortener_type = response['shortener_src']
    user_response_url = response['url'].lower()

    # Shorten url    
    user_response_obj = UrlShortener(user_response_shortener_type, user_response_url) 
    shortened_url = user_response_obj.get_shorten_url()
    print(shortened_url)



# https://learnpython.com/blog/how-to-use-virtualenv-python/
# https://www.askpython.com/python/examples/url-shortener
# https://pyshorteners.readthedocs.io/en/latest/apis.html
# https://medium.com/@nabulovivian2014/how-i-created-a-command-line-application-with-python-edf332b8d414
# https://realpython.com/pyinstaller-python/
