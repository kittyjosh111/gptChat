# SST-05 Voice Module
#
# An attempt to use the SST-05's bridging mode to allow for Text to Speech
# This script requires sst05.py to be run in bridge mode, so that this script may read the
# ai_file in order to pass it into piper-tts.
# This script and sst05 should be in the same directory, or made to look at the same files.
# To start this script, refer to the last few lines invoking the start function.

import os
import time
import numpy as np
import sounddevice as sd
from piper.voice import PiperVoice

def string_save(filename, input):
  """Function to save a string to a file.
  Takes in an INPUT (string), and overwrites to FILENAME (string)"""
  with open(filename, "w") as file:
    file.write(input)

def piper_talk(string, piper_model):
  piper_voice = PiperVoice.load(piper_model)
  stream = sd.OutputStream(samplerate=piper_voice.config.sample_rate, channels=1, dtype='int16')
  stream.start()
  for audio_bytes in piper_voice.synthesize_stream_raw(string):
    int_data = np.frombuffer(audio_bytes, dtype=np.int16)
    stream.write(int_data)
  stream.stop()
  stream.close()
  return string

def start(piper_model, ai_file):
  while True: #infinite loop
    last_modified=os.path.getmtime(ai_file)
    print("[sst05-voice.py] DEBUG: Waiting for AI input...")
    while last_modified == os.path.getmtime(ai_file):
      time.sleep(2.0) #adjust as necessary as to not burn out your processor
    else:
      with open(ai_file, "r") as read:
        ai_text = read.read().rstrip()
      if ai_text: #make sure its not blank
        print("[sst05-voice.py] DEBUG: ai input found:", ai_text)
        piper_talk(ai_text, piper_model)
    string_save(ai_file, "")

## Initiate the script. Modify as needed. ##
## You will need to obtain a piper voice model. Look at their github for more info.
start("./en_US-hfc_female-medium.onnx", "ai_file")