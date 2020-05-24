from flask import Flask , render_template, request, Blueprint, redirect, url_for, flash
from flask import *
import pandas as pd
import io
import csv
import os
from werkzeug.utils import secure_filename
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import requests

global api_key
api_key='hdrgkw8o0kjln629avkxgwgpmlch3iv8edypwavw'

app = Flask(__name__)

def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = "".join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(wordnet_lemmatizer.lemmatize(word) for word in punc_free.split())
    return normalized

def sentence_sentiment(data):
    sentiment_polarity = analyzer.polarity_scores(data)
    if sentiment_polarity['compound'] > 0:
        return 'positive'
    elif sentiment_polarity['compound'] < 0:
        return 'negative'
    else:
        return 'neutral'


@app.route('/')
def load():
    return render_template('index.html')

@app.route('/sentiment_analysis', methods=['GET'])
def sentiment():
    if request.method == 'GET':
        print(request.args)
        print('run this after')
        return 'ok'
        ticker = request.args.get('ticker')
        print(ticker)
        url = ('https://stocknewsapi.com/api/v1?tickers={0}&items=50&token={1}'.format(ticker,api_key))
        r = requests.get(url)
        x = r.json()
        print(x)
        df = pd.DataFrame(x['data'])
        df = df[['title', 'text', 'source_name', 'date']]
        df['date'] = pd.to_datetime(df['date'])
        analyzer = SentimentIntensityAnalyzer()
        df['sentiment']  = df.apply(lambda row: sentence_sentiment(row['text']),axis=1)
        df1 = df.groupby([df['date'].dt.date,df['sentiment']]).size().reset_index(name='count')
        df2 = df.groupby(df['sentiment']).size()
    return {'date_group_by': df1.to_json(), 'sentiment_analysis': df2.to_json()} 

if __name__ == "__main__":
     app.run(debug = True,host='0.0.0.0', port=5000 )

