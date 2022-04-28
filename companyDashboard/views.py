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

predictions = {'msft': [256.4, 239.08, 217.65, 198.61, 183.93],
                'googl': [2111.5, 1917.43, 1754.91, 1631.58, 1535.66],
                'fb': [174.53, 173.46, 172.46, 171.55, 170.7],
                'aapl': [140.54, 123.62, 108.05, 95.22, 84.91],
                'amzn': [2684.32, 2559.47, 2444.67, 2340.24, 2239.31],
                'nflx': [203.3, 208.37, 215.34, 222.06, 227.91]}

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
                prediction = companyPrediction[24 - (int(str(datetime.date.today()).split("-")[2]) - 1)]
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
    # consumer_key = 'p1c4TOG04CIlYFGSbjRdBQr98'
    # consumer_secret = 'lf29kiY3mXdW0FLgvnFIaT0F9vjsNgeM49DbMseBCppsHzwQtm'
    # access_token = '1354062104139952130-goNdDKZ7Hn66cSXvO6jLaQce2mELAE'
    # access_token_secret = '51uilEwpSGQcZnAM7AwuIpxkzHPU9AIa2Geppigjl5R1U'
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
    newsapi = NewsApiClient(api_key='bc7e81851ccf4221b6edaf48941a9888')
    top_headlines = newsapi.get_top_headlines(q=queryMaker[query],
                                        # sources='bbc-news,the-verge',
                                        # category='business',
                                        language='en',
                                        # country='us'
                                        )
    news = top_headlines
    print(news, queryMaker[query])

    # news = [{'articles': [{'author': 'Verge Staff',
    #             'content': 'Come on in, the windows are fine\r\nIf you buy something from a Verge link, Vox Media may earn a commission. See our ethics statement.\r\nMicrosofts next version of Windows, Windows 11, is coming October… [+17914 chars]',
    #             'description': 'Microsoft’s next version of Windows, Windows 11, is coming October 5th. Technically, a near-final version is already here, and we’ve spent considerable time with it on over a dozen different PCs.',
    #             'publishedAt': '2021-10-02T15:00:00Z',
    #             'source': {'id': 'the-verge', 'name': 'The Verge'},
    #             'title': 'Windows 11 seems okay',
    #             'url': 'https://www.theverge.com/22705148/windows-11-upgrade-beta-release-preview-impressions',
    #             'urlToImage': 'https://cdn.vox-cdn.com/thumbor/p_u0ZlnLrGczT6gT7lTppXCub3M=/0x178:2560x1518/fit-in/1200x630/cdn.vox-cdn.com/uploads/chorus_asset/file/22894952/twarren__windows11_sharper.jpg'}],
    #         'status': 'ok',
    #         'totalResults': 1},
    #         {'articles': [{'author': 'Verge Staff',
    #             'content': 'Come on in, the windows are fine\r\nIf you buy something from a Verge link, Vox Media may earn a commission. See our ethics statement.\r\nMicrosofts next version of Windows, Windows 11, is coming October… [+17914 chars]',
    #             'description': 'Microsoft’s next version of Windows, Windows 11, is coming October 5th. Technically, a near-final version is already here, and we’ve spent considerable time with it on over a dozen different PCs.',
    #             'publishedAt': '2021-10-02T15:00:00Z',
    #             'source': {'id': 'the-verge', 'name': 'The Verge'},
    #             'title': 'Windows 11 seems okay',
    #             'url': 'https://www.theverge.com/22705148/windows-11-upgrade-beta-release-preview-impressions',
    #             'urlToImage': 'https://cdn.vox-cdn.com/thumbor/p_u0ZlnLrGczT6gT7lTppXCub3M=/0x178:2560x1518/fit-in/1200x630/cdn.vox-cdn.com/uploads/chorus_asset/file/22894952/twarren__windows11_sharper.jpg'}],
    #         'status': 'ok',
    #         'totalResults': 1}]
    return news['articles']
