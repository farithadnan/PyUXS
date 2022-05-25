import json
import requests
import pyshorteners
from modules.clihelper import GlobalHelper


# Handling user response
class UserResponseFilter(object):

    def __init__(self, userResponse):
        self.shortener = pyshorteners.Shortener()
        self.userResponse = userResponse

    # Method to shorten url
    def get_shorten_url(self):
        shortenerType = self.userResponse['shortener_src']
        shortenerUrl = self.userResponse['url']
        
        try:
            response = requests.get(shortenerUrl)
            shorter = ShortenerTypeFilter(shortenerUrl)

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
class ShortenerTypeFilter(object):
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



