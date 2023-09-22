import openai
import speech_recognition as sr
import pyttsx3
from dotenv import dotenv_values

# call the api key
openai.api_key = dotenv_values('OPENAI_API_KEY')

# tts engine
engine = pyttsx3.init()

# function listens for an audio input. If recognized, respond using OpenAI
def listen_for_response():
    
    # speech recognizer
    r = sr.Recognizer()
    
    # listen for input
    with sr.Microphone() as source:
        audio = r.listen(source)

    # try for recognizing audio
    try:
        prompt = r.recognize_google(audio, language="en=US", show_all=False)
        print(prompt)

        # OpenAI response
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temp=.7,
            max_tokens=300
        )

        # text response
        text_response = str(response['choices'][0]['text']).strip('\n\n')
        print(text_response)

        # tts response
        engine.say(text_response)
        engine.runAndWait()
        print()

    # catch to recognize fails
    except sr.UnknownValueError:
        text_response = "Speech Recognition: Sorry, could you please repeat that."
        print(text_response)
        engine.say(text_response)
        engine.runAndWait()
        print()
    
    except sr.RequestError as e:
        print("Speech Recognition: Request not found from Google's Speech Recognition Services; {0}".format(e))


def main():
    while True:
        listen_for_response()

if __name__ == "__main__":
    main()