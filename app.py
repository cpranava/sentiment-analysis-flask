from flask import *
from flask_cors import CORS,cross_origin
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
model = None
app = Flask(__name__)
CORS(app)

global analyzer
analyzer = SentimentIntensityAnalyzer()


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
def home_endpoint():
    return 'Hello! This is my flask API endpoint'


@app.route('/sentiment_analysis', methods=['GET'])
def get_prediction():
    # Works only for a single sample
    if request.method == 'GET':
        ticker = request.args.get('ticker')
        url = ('https://stocknewsapi.com/api/v1?tickers={0}&items=50&token={1}'.format(ticker,api_key))
        r = requests.get(url)
        x = r.json()
        df = pd.DataFrame(x['data'])
        df = df[['title', 'text', 'source_name', 'date']]
        df['date'] = pd.to_datetime(df['date'])
        analyzer = SentimentIntensityAnalyzer()
        df['sentiment']  = df.apply(lambda row: sentence_sentiment(row['text']),axis=1)
        df1 = df.groupby([df['date'].dt.date,df['sentiment']]).size().unstack(fill_value=0).stack().reset_index(name='count')
        df1['date'] = pd.to_datetime(df1['date']).dt.strftime('%Y-%m-%d')
        df2 = df.groupby(df['sentiment']).size()
    return {'date_group_by': df1.to_json(orient='records'), 'sentiment_analysis': df2.to_json()}


if __name__ == "__main__":
     app.run(debug = True,host='0.0.0.0', port=5000 )

