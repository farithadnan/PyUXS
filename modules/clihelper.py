import os
import time

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
        os.system("python main.py")
        time.sleep(0.2)
        return quit()

    # invalid restart func
    def invalid_restart():
        print("\nInvalid URL! Please try again.")
        input("Click any key to restart...\n")
        print ("Restarting...")
        os.system("python main.py")
        time.sleep(0.2) 
        return quit()
