import ollama

def generate_response(host, model, prompt, streaming=True):
  client = ollama.Client(
    host=host
  )
  output = ollama.generate(
    model=model,
    prompt=prompt,
    strem=streaming
  )
  return output['response']
