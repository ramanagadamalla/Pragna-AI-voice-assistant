import openai
import pyttsx3

# Set up the OpenAI API
openai.api_key = "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"
model_engine = "text-davinci-002"

# Set up the text-to-speech engine
voice_engine = pyttsx3.init()

def chat_with_gpt(text):
    # Call the OpenAI API to generate a response
    response = openai.Completion.create(
        engine=model_engine,
        prompt=text,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )

    # Extract the generated response from the API response
    message = response.choices[0].text.strip()

    # Speak the response using text-to-speech
    voice_engine.say(message)
    voice_engine.runAndWait()

# Example usage
while True:
    text_input = input("You: ")
    chat_with_gpt(text_input)
