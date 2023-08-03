import win32com.client as wincl
import openai
import requests
import json

speak = wincl.Dispatch("SAPI.SpVoice")

# Setup OpenAI API Key
openai.api_key = "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"

# Define a function to generate text from OpenAI API
def generate_text(prompt):
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )

    message = response.choices[0].text
    return message.strip()

# Define a function to process user's voice command
def process_command(command):
    if "hello" in command.lower():
        return "Hello, how can I assist you?"

    if "weather" in command.lower():
        api_key = "<INSERT_YOUR_WEATHER_API_KEY_HERE>"
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        city_name = "<INSERT_YOUR_CITY_NAME_HERE>"
        complete_url = base_url + "appid=" + api_key + "&q=" + city_name
        response = requests.get(complete_url)
        data = response.json()
        if data["cod"] != "404":
            temperature = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            return f"The temperature in {city_name} is {temperature} Kelvin and the humidity is {humidity}%."
        else:
            return "Unable to get weather data."

    # Use OpenAI API to generate a response for other commands
    prompt = command + "\nAI:"
    return generate_text(prompt)

# Define a function to listen to user's voice command
def listen():
    speak.Speak("How can I assist you?")
    recognizer = wincl.Dispatch("SAPI.SpSharedRecognizer")
    recognizer.AudioInputStream = wincl.Dispatch("SAPI.SpMMAudioIn")
    recognition = recognizer.Recognize()
    return recognition.PhraseInfo.GetText()

# Define the main function to run the voice assistant
def run():
    while True:
        try:
            command = listen()
            if command:
                response = process_command(command)
                speak.Speak(response)
        except:
            speak.Speak("Sorry, I didn't get that. Can you please repeat?")
            continue

if __name__ == "__main__":
    run()
