import json
from PyInquirer import prompt
from modules.clihelper import GlobalHelper
from modules.clifilter import UserResponseFilter


# Prompt questions to determine whether to shorten or expand url
class PromptQuestion(object):
    def __init__(self, response):
        self.userResponse = response

    # Filter user response, and filter based on user option
    def handleUserResponse(self):
        if ('mode_type' in self.userResponse):

            if (self.userResponse['mode_type'] == 'Shorten'):
                question_shortener_type = json.loads(open('questions/shorten_question.json').read())
                response_shortener_type = prompt(question_shortener_type)

                # process to shorten url
                shortenResponse = UserResponseFilter(response_shortener_type)
                return shortenResponse.get_shorten_url()
            elif (self.userResponse['mode_type'] == 'Expand'):
                question_expand_type = json.loads(open('questions/expand_question.json').read())
                response_expand_type = prompt(question_expand_type)

                # process to expand url
                expandResponse = UserResponseFilter(response_expand_type)
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
