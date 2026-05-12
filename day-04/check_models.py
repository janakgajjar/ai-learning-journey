from google import genai

client = genai.Client(api_key="AIzaSyAJ5Bkq5SDDEN4z5CIkglZ1YgY7QJ6vCpY")

for model in client.models.list():
    print(model.name)