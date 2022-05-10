from audioop import rms
import re
from django.shortcuts import render
from django.contrib import messages
import yfinance 
import tweepy as tw
from tweepy import OAuthHandler
import datetime
from newsapi import NewsApiClient
import datetime
import pandas as pd
import numpy as np
import re
from textblob import TextBlob
from matplotlib import pyplot as plt

predictions = {'msft': [258.62, 236.78, 214.29, 195.66, 182.4],
                'googl': [2088.56, 1884.71, 1718.84, 1596.58, 1503.79],
                'fb': [200.22, 200.12, 199.73, 199.2, 198.62],
                'aapl': [141.95, 125.0, 109.79, 97.39, 87.5],
                'amzn': [2242.34, 2161.89, 2075.04, 1979.22, 1886.33],
                'nflx': [204.28, 209.17, 214.78, 219.59, 223.28]}

rmse = {
        'msft': 20.45,
        'googl': 162.14,
        'fb': 19.92,
        'aapl': 10.27,
        'amzn': 165.28,
        'nflx': 23.17
        }
# Create your views here.
def dashboard(request):
    listedCompany = ['NASDAQ:MSFT', 'NASDAQ:GOOGL', 'NASDAQ:FB', 'NASDAQ:AAPL','NASDAQ:NFLX','NASDAQ:AMZN']
    if not request.user.is_anonymous:
        if request.method == 'POST':
            ticker = request.POST['ticker']
            if ticker.upper() in listedCompany:
                month = str(datetime.date.today()).split("-")[1]
                url1 = 'companyDashboard/images/' + ticker.split(':')[1].lower() + '/performance/' + ticker.split(':')[1].upper() + month + '.png'
                url2 = 'companyDashboard/images/' + ticker.split(':')[1].lower() + '/nxt30days/' + ticker.split(':')[1].upper() + month + '.png'
                # print(url1, url2)
                getInfo = yfinance.Ticker(ticker.split(':')[1].upper())
                prices = {
                    'open': getInfo.info['open'],
                    'current': getInfo.info['currentPrice'],
                    'high': getInfo.info['dayHigh'],
                    'low': getInfo.info['dayLow']
                }
                tweetObj = tweet(ticker.split(':')[1].upper())
                newsObj = news(ticker.split(':')[1].upper())
                url3 = "companyDashboard/images/" + ticker.split(':')[1].lower() + "/scatterplot/sentimentAnalysis.png"
                url4 = "companyDashboard/images/" + ticker.split(':')[1].lower() + "/barplot/sentimentAnalysis.png"
                # prediction = predictions[int(str(datetime.date.today()).split("-")[2]) - 1]
                companyPrediction = predictions[ticker.split(':')[1].lower()]
                prediction = companyPrediction[5 - int(str(datetime.date.today()).split("-")[2])]
                # print(posNegCnt)
                lastDayPrice = yfinance.Ticker(ticker.split(':')[1].upper()).history(period="5d")["Close"].iloc[-1]
                # print(lastDayPrice)
                diff = "increase" if (prediction - lastDayPrice) > 0 else "decrease"
                posCnt = "more" if posNegCnt["Positive"] > posNegCnt["Negative"] else "less"
                if diff == "decrease" and posCnt == "less":
                    declaration = f"As per the model, there is a {diff} in closing price and there are {posCnt} positive tweets, model says that there is a downward trend."
                elif diff == "increase" and posCnt == "more":
                    declaration = f"As per the model, there is an {diff} in closing price and there are {posCnt} positive tweets, model says that there is an upward trend."
                else:
                    declaration = f"As per the model, there is an {diff} in closing price but there are {posCnt} positive tweets, model says that the trend is stagnant."
                sd = rmse[ticker.split(':')[1].lower()]
                context = {
                    'ticker': ticker,
                    'url1': url1,
                    'url2': url2,
                    'url3': url3,
                    'url4': url4,
                    'prices':prices,
                    'tweetObj': tweetObj,
                    'newsObj': newsObj,
                    'prediction': prediction,
                    'declaration': declaration,
                    'sd': sd
                }
                return render(request, 'companyDashboard/dashboard.html', context)
        else:
            # print("Kya re")
            pass
    else:
        messages.error(request, 'You are not authenticated')
        return render(request, 'home/base.html')
    return render(request, 'companyDashboard/dashboard.html')

def cleanTxt(text):
    text = re.sub(r'@[A-Za-z0-9]', '', text)
    text = re.sub(r'#', '', text)
    text = re.sub(r'RT[\s]+', '', text)
    text = re.sub(r'https?:\/\/\S+', '', text)
    return text

def getSubjectivity(text):
    return TextBlob(text).sentiment.subjectivity

def getPolarity(text):
    return TextBlob(text).sentiment.polarity

def getAnalysis(score):
    if score < 0:
        return "Negative"
    elif score > 0:
        return "Positive"
    else:
        return "Neutral"

def tweet(query):
    # consumer_key = ''
    # consumer_secret = ''
    # access_token = ''
    # access_token_secret = ''
    # auth = tw.OAuthHandler(consumer_key, consumer_secret)
    # auth.set_access_token(access_token, access_token_secret)
    # api = tw.API(auth)

    # tweetsObj = api.search_tweets(q = query, count = 20, lang='en')
    # tweets = [tweet._json for tweet in tweetsObj]
    tweets = [
        {'created_at': 'Oct. 3, 2021, 3:23 a.m.', 'text': 'RT @IamRenganathan: Life is short get your name in the hall of fame Google, Apple, Microsft, Netflix, Amazon, and Facebook.'},
        {'created_at': 'Oct. 2, 2021, 7:43 p.m.', 'text': '@TMessi_1 @Porkchop_EXP @Cernovich So microsft flight sim is for kids? tell that to the pilots that use it to train.'},
        {'created_at': 'Oct. 2, 2021, 7:43 p.m.', 'text': '@TMessi_1 @Porkchop_EXP @Cernovich Wow! Im so happy'},
        {'created_at': 'Oct. 2, 2021, 7:43 p.m.', 'text': '@TMessi_1 @Porkchop_EXP @Cernovich Damn! I just hate you!!'}
    ]
    df = pd.DataFrame([t['text'] for t in tweets], columns=["Tweets"])
    df['Tweets'] = df['Tweets'].apply(cleanTxt)
    df["Subjectivity"] = df["Tweets"].apply(getSubjectivity)
    df["Polarity"] = df["Tweets"].apply(getPolarity)
    df["Analysis"] = df["Polarity"].apply(getAnalysis)
    global posNegCnt
    posNegCnt = df["Analysis"].value_counts()
    if "Positive" not in posNegCnt:
        posNegCnt["Positive"] = 0
    if "Negative" not in posNegCnt:
        posNegCnt["Negative"] = 0
    print(posNegCnt)
    plt.figure(figsize=(8,6))
    for i in range(0, df.shape[0]):
        plt.scatter(df['Polarity'][i], df['Subjectivity'][i], color='Blue')
    plt.title('Sentiment Analysis')
    plt.xlabel('Polarity')
    plt.ylabel('Subjectivity')
    sentimentAnalysis1Loc = "companyDashboard/static/companyDashboard/images/" + query.lower() + "/scatterplot/sentimentAnalysis.png"
    sentimentAnalysis2Loc = "companyDashboard/static/companyDashboard/images/" + query.lower() + "/barplot/sentimentAnalysis.png"    
    plt.savefig(sentimentAnalysis1Loc)
    plt.title("Sentiment Analysis")
    plt.xlabel('Sentiment')
    plt.ylabel('Counts')
    df['Analysis'].value_counts().plot(kind="bar")
    plt.savefig(sentimentAnalysis2Loc)
    return tweets

def news(query):
    queryMaker = {
        "MSFT": "microsoft",
        "NFLX": "netflix",
        "AAPL": "apple",
        "FB": "facebook",
        "GOOGL": "google",
        "AMZN": "amazon"
    }
    # newsapi = NewsApiClient(api_key='')
    # top_headlines = newsapi.get_top_headlines(q=queryMaker[query],
    #                                     # sources='bbc-news,the-verge',
    #                                     # category='business',
    #                                     language='en',
    #                                     # country='us'
    #                                     )
    # news = top_headlines
    # print(news, queryMaker[query])
    # return news['articles']

    news = {'status': 'ok', 'totalResults': 1, 'articles': [{'source': {'id': 'the-times-of-india', 'name': 'The Times of India'}, 'author': 'Ayushmann Chawla', 'title': 'WhatsApp may get Instagram-style quick reactions feature for status updates - Times of India', 'description': 'Facebook CEO Mark Zuckerberg recently announced new features for WhatsApp messaging platform such as message reactions, Communities and others. Now as', 'url': 'https://timesofindia.indiatimes.com/gadgets-news/whatsapp-may-get-instagram-style-quick-reactions-feature-for-status-updates/articleshow/91178789.cms', 'urlToImage': 'https://static.toiimg.com/thumb/msid-91178744,width-1070,height-580,imgsize-983013,resizemode-75,overlay-toi_sw,pt-32,y_pad-40/photo.jpg', 'publishedAt': '2022-04-29T10:36:00Z', 'content': None}, {'source': {'id': 'the-times-of-india', 'name': 'The Times of India'}, 'author': 'Ayushmann Chawla', 'title': 'WhatsApp may get Instagram-style quick reactions feature for status updates - Times of India', 'description': 'Facebook CEO Mark Zuckerberg recently announced new features for WhatsApp messaging platform such as message reactions, Communities and others. Now as', 'url': 'https://timesofindia.indiatimes.com/gadgets-news/whatsapp-may-get-instagram-style-quick-reactions-feature-for-status-updates/articleshow/91178789.cms', 'urlToImage': 'https://static.toiimg.com/thumb/msid-91178744,width-1070,height-580,imgsize-983013,resizemode-75,overlay-toi_sw,pt-32,y_pad-40/photo.jpg', 'publishedAt': '2022-04-29T10:36:00Z', 'content': None}, {'source': {'id': 'the-times-of-india', 'name': 'The Times of India'}, 'author': 'Ayushmann Chawla', 'title': 'WhatsApp may get Instagram-style quick reactions feature for status updates - Times of India', 'description': 'Facebook CEO Mark Zuckerberg recently announced new features for WhatsApp messaging platform such as message reactions, Communities and others. Now as', 'url': 'https://timesofindia.indiatimes.com/gadgets-news/whatsapp-may-get-instagram-style-quick-reactions-feature-for-status-updates/articleshow/91178789.cms', 'urlToImage': 'https://static.toiimg.com/thumb/msid-91178744,width-1070,height-580,imgsize-983013,resizemode-75,overlay-toi_sw,pt-32,y_pad-40/photo.jpg', 'publishedAt': '2022-04-29T10:36:00Z', 'content': None}]}
    return news['articles']
