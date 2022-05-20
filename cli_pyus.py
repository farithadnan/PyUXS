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
class FilterResponse(object):

    def __init__(self, userResponse):
        self.shortener = pyshorteners.Shortener()
        self.userResponse = userResponse

    # Method to shorten url
    def get_shorten_url(self):
        shortenerType = self.userResponse['shortener_src']
        shortenerUrl = self.userResponse['url']

        try:
            response = requests.get(shortenerUrl)
            shorter = ShortenerType(shortenerUrl)

            if response.status_code != 404:
                switcher = {
                    'TinyURL': shorter.tinyUrl,
                    'Chilp.it': shorter.chilpit,
                    'Da.gd': shorter.dagd
                }
                func = switcher.get(shortenerType, lambda: "Invalid shortener! Please try again.")
                return func()
        except:
                return "Invalid URL! Please try again."
    
    # Method to expand shorten url
    def get_expand_url(self):
        expandUrl = self.userResponse['url']
        try:
            response = requests.get(expandUrl)
            if response.status_code != 404:
                urlExpander = requests.head(expandUrl, allow_redirects=True).url
                return urlExpander
        except:
            return "Invalid URL! Please try again."
    

# Class to handle shortener type
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


# Prompt questions to determine whether to shorten or expand url
class PromptQuestion(object):
    def __init__(self, modeType):
        self.modeType = modeType['mode_type']

    # Filter user response, and filter based on user option
    def filterResponse(self):
        
        if (self.modeType == 'Shorten'):
            question_shortener_type = json.loads(open('questions/shorten_question.json').read())
            response_shortener_type = prompt(question_shortener_type)

            # process to shorten url
            shortenResponse = FilterResponse(response_shortener_type)
            return shortenResponse.get_shorten_url()
        else:
            question_expand_type = json.loads(open('questions/expand_question.json').read())
            response_expand_type = prompt(question_expand_type)

            # process to expand url
            expandResponse = FilterResponse(response_expand_type)
            return expandResponse.get_expand_url()
    

# Main function
if __name__ == '__main__':

    # Welcome message
    cprint(figlet_format('PyUXS', font='slant'))
    print("Welcome to PyUXS!\n")

    # Startup questions
    question_mode_type = json.loads(open('questions/startup_question.json').read())
    response_mode_type = prompt(question_mode_type)

    # Process user response and process url
    fetchObj = PromptQuestion(response_mode_type)
    finalResult = fetchObj.filterResponse()
    print(finalResult)



# https://learnpython.com/blog/how-to-use-virtualenv-python/
# https://www.askpython.com/python/examples/url-shortener
# https://pyshorteners.readthedocs.io/en/latest/apis.html
# https://medium.com/@nabulovivian2014/how-i-created-a-command-line-application-with-python-edf332b8d414
# https://realpython.com/pyinstaller-python/
