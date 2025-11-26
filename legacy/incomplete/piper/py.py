import os
import ollama
import piper
import numpy as np
import sounddevice as sd
from piper.voice import PiperVoice

client = ollama.Client(host='http://localhost:11434') #This points the script to the remote ollama API

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

def ollama_response(model, prompt):
  """Have the AI generate a response given the MODEL and PROMPT"""
  output = client.generate( #instead of ollama.generate, we use client.generate
    model=model,
    prompt=prompt
  )
  return output['response']

def ollama_to_piper(model, prompt, piper_model):
  generated_out = ollama_response(model, prompt)
  print(generated_out)
  return piper_talk(generated_out, piper_model)

def start_loop(model, piper_model):
  while True:
    user_input = input('User: ')
    #convo = [{'role': 'user', 'content': f'{user_input}'}]
    ollama_to_piper(model, user_input, piper_model)

model_1="llama3.2"
piper_model_1="en_US-kristin-medium.onnx"

start_loop(model_1, piper_model_1)
