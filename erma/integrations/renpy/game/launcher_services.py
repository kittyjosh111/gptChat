#!/usr/bin/python3
import threading
import subprocess

def launcher(filename):
    """Function that takes in a FILENAME which should be a python file to run"""
    subprocess.run(["python", filename])

def start(sentiment=True):
    """Main function. Launches erma.py.
    Additionally, if SENTIMENT is true, it launches sentiment.py"""
    launch_erma = threading.Thread(target=launcher, args=("erma.py", )) #and erma
    launch_erma.start()
    if sentiment:
        launch_sentiment = threading.Thread(target=launcher, args=("sentiment.py", )) #prepare sentiment
        launch_sentiment.start()
    print("Launcher started!")
