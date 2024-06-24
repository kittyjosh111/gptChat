#!/usr/bin/python3
"""Sentiment Analysis script.
Requires torch and transformers to run the analysis.
Reads changes in ai_text, then runs sentiment analysis on it, then write
to a file named "sentiment", for use in Ren'Py scripts.rpy"""

import os
import time
from transformers import pipeline #its huggingface time

def string_save(filename, input):
  """Function to save a string to a file.
  Takes in an INPUT (string), and overwrites to FILENAME (string)"""
  with open(filename, "w") as file:
    file.write(input)

def start(model, ai_file):
    string_save("sentiment", "") #create (or blank) out this file
    print("DEBUG: sentiment cleared. waiting for ai input...")
    while True: #infinite loop
        last_modified=os.path.getmtime(ai_file)
        while last_modified == os.path.getmtime(ai_file):
            time.sleep(2.0) #adjust as necessary as to not burn out your processor
        else:
            with open(ai_file, "r") as read:
                ai_text = read.read().rstrip()
            if ai_text: #make sure its not blank
                print("DEBUG: ai input found:", ai_text)
                sentiment_pipeline = pipeline(model=model) #load the model
                eval_sentiment = sentiment_pipeline([ai_text])[0]['label'] #run it, extract sentiment
                print("DEBUG: sentiment:", eval_sentiment)
                time.sleep(2.0) #sometimes, we write it just too fast that scripts.rpy fails to log the original time
                string_save("sentiment", eval_sentiment) #write to file

## Initiate the script. Modify as needed. ##
start("MarieAngeA13/Sentiment-Analysis-BERT", "neuralcloud_ai.file") #this uses the model defined and looks at ai_file as "neuralcloud_ai.file"
