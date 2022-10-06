import requests
import sys
import re
import nltk
import os
from dotenv import load_dotenv
import textblob

load_dotenv()

nltk.download('stopwords')

from nltk.corpus import stopwords


hed = {'Authorization': 'Bearer ' + os.environ.get("twitterBearerToken")}

url = 'https://api.twitter.com/2/tweets/search/recent?query=from:'

username = 'time'

if len(sys.argv)>1:
    result=f'{url}{sys.argv[1]}'

else:
    result = f'{url}{username}'    

response = requests.get(result, headers=hed)
result_dict =  response.json()      


def cleaningData(dataToBeCleaned): 
    return re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", dataToBeCleaned)

def removeStopWords(dataToBeCleaned):
    setOfWords = set(stopwords.words('english'))
    return ' '.join([i for i in dataToBeCleaned.split() if i not in setOfWords])

def getTextSentiment(text):
    analysis = textblob.TextBlob(text)
    return analysis.sentiment.polarity


    

for i in result_dict['data']:

    cleanedText = cleaningData(i['text'])
    cleanedText = removeStopWords(cleanedText)
    p = getTextSentiment(cleanedText)
    if p>0:
        print(f"POS--------{cleanedText}")
    elif p==0:
        print(f"NEUTRAL--------{cleanedText}")
    else:
        print(f"NEGATIVE--------{cleanedText}")
    






