import PyPDF3
import azure.cognitiveservices.speech as sdk
import requests
import os
import azure.cognitiveservices.speech as speechsdk
key = "08118a610f8d40cf844e9f0e3d252fbe"  #make sure to replace this with your own API key
region = "centralindia"  # make sure to replace this with your own service region
source_language="en-US"
target_language="mr"
endpoint="https://ltr.cognitiveservices.azure.com/"

config = sdk.SpeechConfig(subscription=key, region=region)
synthesizer = sdk.SpeechSynthesizer(speech_config=config)

book = open("Gouss_Resume 100 (1).pdf","rb")
reader = PyPDF3.PdfFileReader(book)
#print(book)

for num in range(0,reader.numPages):
    text = reader.getPage(num).extractText() 
    result = synthesizer.speak_text_async(text).get()
    print(text)

def translate(text, source_language, target_language, key, region, endpoint):
    # Use the Translator translate function
    url = endpoint + '/translate'
    # Build the request
    params = {
        'api-version': '3.0',
        'from': source_language,
        'to': target_language
    }
    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': region,
        'Content-type': 'application/json'
    }
    body = [{
        'text': text
    }]
    # Send the request and get response
    request = requests.post(url, params=params, headers=headers, json=body)
    response = request.json()
    # Get translation
    translation = response[0]["translations"][0]["text"]
    # Return the translation

    print()

    return translation
