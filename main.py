from __future__ import print_function, unicode_literals
import sys
import json
from PyInquirer import prompt
from colorama import init
init(strip=not sys.stdout.isatty())  # strip colors if stdout is redirected
from termcolor import cprint
from pyfiglet import figlet_format
from modules.cliprompt import PromptQuestion


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
    finalResult = fetchObj.handleUserResponse()
    print(finalResult + "\n")

    # End Msg Confirmation
    question_end_msg = json.loads(open('questions/endgame_question.json').read())
    response_end_msg = prompt(question_end_msg)
    promptObj = PromptQuestion(response_end_msg)
    promptObj.handleUserResponse()

