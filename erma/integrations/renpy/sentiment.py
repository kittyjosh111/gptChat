#!/usr/bin/python3
""" Sentiment Analysis script.
Requires torch and transformers to run the analysis.
Reads changes in ai_text, then runs sentiment analysis on it, then write
to a file named "sentiment", for use in Ren'Py scripts.rpy"""

import os
import time
from erma import string_save
from transformers import pipeline

def start(model, ai_file):
    string_save("sentiment", "") #create (or blank) out this file
    while True: #infinite loop
        last_modified=os.path.getmtime(ai_file)
        while last_modified == os.path.getmtime(ai_file):
            time.sleep(2.0) #adjust as necessary as to not burn out your processor
            print("DEBUG: waiting for ai input...")
        else:
            with open(ai_file, "r") as read:
                ai_text = read.read().rstrip()
            if ai_text: #make sure its not blank
                print("DEBUG: ai input found:", ai_text)
                sentiment_pipeline = pipeline(model=model) #load the model
                eval_sentiment = sentiment_pipeline([ai_text])[0]['label'] #run it, extract sentiment
                print("DEBUG: sentiment:", eval_sentiment)
                string_save("sentiment", eval_sentiment) #write to file

## Initiate the script. Modify as needed. ##
#start("MarieAngeA13/Sentiment-Analysis-BERT", "neuralcloud_ai.file") #this uses the model defined and looks at ai_file as "neuralcloud_ai.file"
