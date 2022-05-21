from __future__ import print_function, unicode_literals
import os
import sys
import json
import time
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
                print("\nDone! Here's your shortened URL:")
                switcher = {
                    'TinyURL': shorter.tinyUrl,
                    'Chilp.it': shorter.chilpit,
                    'Da.gd': shorter.dagd,
                }
                func = switcher.get(shortenerType, lambda: "Invalid shortener! Please try again.")
                return func()
        except:    
                return GlobalHelper.invalid_restart()
    
    # Method to expand shorten url
    def get_expand_url(self):
        expandUrl = self.userResponse['url']
        try:
            response = requests.get(expandUrl)
            if response.status_code != 404:
                print("\nDone! Here's your expanded URL:")
                urlExpander = requests.head(expandUrl, allow_redirects=True).url
                return urlExpander
        except:
            return GlobalHelper.invalid_restart()
    




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
    def __init__(self, response):
        self.userResponse = response

    # Filter user response, and filter based on user option
    def filterResponse(self):
        if ('mode_type' in self.userResponse):

            if (self.userResponse['mode_type'] == 'Shorten'):
                question_shortener_type = json.loads(open('questions/shorten_question.json').read())
                response_shortener_type = prompt(question_shortener_type)

                # process to shorten url
                shortenResponse = FilterResponse(response_shortener_type)
                return shortenResponse.get_shorten_url()
            elif (self.userResponse['mode_type'] == 'Expand'):
                question_expand_type = json.loads(open('questions/expand_question.json').read())
                response_expand_type = prompt(question_expand_type)

                # process to expand url
                expandResponse = FilterResponse(response_expand_type)
                return expandResponse.get_expand_url()
            else:
                return GlobalHelper.exiting_cli()

        elif ('endgame' in self.userResponse):
            if (self.userResponse['endgame'] == 'Yes'):
                return GlobalHelper.restarting_cli()
            elif (self.userResponse['endgame'] == 'No'):
                return GlobalHelper.exiting_cli()
    
        else:
            return GlobalHelper.exiting_cli()



class GlobalHelper:
    # existing function
    def exiting_cli():
        print("\nExiting...")
        print ("Bye!")
        time.sleep(0.2)
        exit()

    # restart function
    def restarting_cli():
        print("\nRestarting...")
        time.sleep(0.2)
        os.system("python cli_pyus.py")
        time.sleep(0.2)
        return quit()

    # invalid restart func
    def invalid_restart():
        print("\nInvalid URL! Please try again.")
        input("Click any key to restart...\n")
        print ("Restarting...")
        os.system("python cli_pyus.py")
        time.sleep(0.2) 

        return quit()



# Main function
if __name__ == '__main__':

    # Welcome message
    cprint(figlet_format('PyUXS', font='slant'))
    print("\tWelcome to PyUXS!")
    print("(Python URL Expander & Shortener)\n")

    # Startup questions
    question_mode_type = json.loads(open('questions/startup_question.json').read())
    response_mode_type = prompt(question_mode_type)

    # Process user response and process url
    fetchObj = PromptQuestion(response_mode_type)
    finalResult = fetchObj.filterResponse()
    print(finalResult + "\n")

    # End Msg Confirmation
    question_end_msg = json.loads(open('questions/endgame_question.json').read())
    response_end_msg = prompt(question_end_msg)
    promptObj = PromptQuestion(response_end_msg)
    promptObj.filterResponse()
