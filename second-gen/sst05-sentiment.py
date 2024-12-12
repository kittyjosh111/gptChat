# SST-05 Sentiment Module
#
# An attempt to use the SST-05's bridging mode to allow for sentiment analysis
# This script requires sst05.py to be run in bridge mode, so that this script may read the
# ai_file in order to pass it into textblob.
# This script and sst05 should be in the same directory, or made to look at the same files.
# To start this script, refer to the last few lines invoking the start function.

import os
import time
from textblob import TextBlob

def string_save(filename, input):
  """Function to save a string to a file.
  Takes in an INPUT (string), and overwrites to FILENAME (string)"""
  with open(filename, "w") as file:
    file.write(input)

def sent_check(text):
  """Function that returns sentiment as "positive",
  "neutral", or "negative" based on the TEXT provided."""
  sent_score = TextBlob(text).sentiment.polarity
  if sent_score > 0:
    return "positive"
  elif sent_score == 0:
    return "neutral"
  else:
    return "negative"

def start(sentiment_file, ai_file):
  while True: #infinite loop
    last_modified=os.path.getmtime(ai_file)
    print("[sst05-sentiment.py] DEBUG: Waiting for AI input...")
    while last_modified == os.path.getmtime(ai_file):
      time.sleep(2.0) #adjust as necessary as to not burn out your processor
    else:
      with open(ai_file, "r") as read:
        ai_text = read.read().rstrip()
      if ai_text: #make sure its not blank
        print("[sst05-sentiment.py] DEBUG: ai input found:", ai_text)
        sentiment = sent_check(ai_text)
        print("[sst05-sentiment.py] DEBUG: sentiment is:", sentiment)
        string_save(sentiment_file, sentiment)
    #string_save(ai_file, "") #might not be necessary for this script

## Initiate the script. Modify as needed. ##
start("sentiment", "ai_file")