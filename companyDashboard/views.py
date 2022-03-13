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
import re
from textblob import TextBlob
from matplotlib import pyplot as plt

predictions = {'msft': [279.18, 254.3, 222.94, 194.37, 173.37, 160.54, 153.72, 150.23, 148.12, 146.3, 144.37, 142.35, 140.47, 139.02, 138.28, 138.44, 139.6, 141.77, 144.89, 148.85, 153.53, 158.79, 164.48, 170.49, 176.7, 183.0, 189.27, 195.43, 201.34, 206.9],
                'googl': [2549.75, 2302.73, 2035.02, 1806.52, 1637.91, 1522.21, 1442.86, 1384.44, 1335.67, 1288.98, 1239.66, 1185.18, 1124.93, 1060.05, 993.13, 927.7, 867.35, 814.9, 771.8, 738.17, 713.09, 695.16, 682.85, 674.74, 669.63, 666.58, 664.87, 663.96, 663.49, 663.2],
                'fb': [208.2, 205.23, 202.32, 199.59, 197.17, 195.07, 193.3, 191.82, 190.6, 189.6, 188.77, 188.09, 187.52, 187.02, 186.59, 186.2, 185.84, 185.52, 185.23, 184.96, 184.73, 184.52, 184.35, 184.21, 184.11, 184.03, 183.99, 183.97, 183.98, 184.01],
                'aapl': [158.78, 151.35, 144.65, 139.31, 135.28, 132.16, 129.5, 126.89, 124.08, 120.98, 117.59, 113.98, 110.22, 106.39, 102.52, 98.62, 94.67, 90.65, 86.53, 82.26, 77.83, 73.23, 68.45, 63.52, 58.49, 53.43, 48.42, 43.56, 38.95, 34.67],
                'amzn': [2873.5, 2596.07, 2358.51, 2161.84, 1982.56, 1836.89, 1728.2, 1653.44, 1606.96, 1581.92, 1572.07, 1572.41, 1579.23, 1589.88, 1602.55, 1616.02, 1629.5, 1642.53, 1654.86, 1666.38, 1677.09, 1687.06, 1696.38, 1705.18, 1713.57, 1721.67, 1729.57, 1737.33, 1745.03, 1752.69],
                'nflx': [392.27, 388.76, 384.19, 379.27, 374.66, 370.73, 367.61, 365.26, 363.53, 362.23, 361.16, 360.17, 359.17, 358.11, 356.96, 355.77, 354.57, 353.41, 352.32, 351.35, 350.49, 349.77, 349.17, 348.68, 348.3, 348.0, 347.78, 347.63, 347.54, 347.51]}
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
                print(url1, url2)
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
                prediction = companyPrediction[int(str(datetime.date.today()).split("-")[2]) - 1]
                context = {
                    'ticker': ticker,
                    'url1': url1,
                    'url2': url2,
                    'url3': url3,
                    'url4': url4,
                    'prices':prices,
                    'tweetObj': tweetObj,
                    'newsObj': newsObj,
                    'prediction': prediction
                }
                return render(request, 'companyDashboard/dashboard.html', context)
        else:
            print("Kya re")
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

    # tweets = api.search_tweets(q = query, count = 2, lang='en')
    tweets = [
        {'created_at': 'Oct. 3, 2021, 3:23 a.m.', 'text': 'RT @IamRenganathan: Life is short get your name in the hall of fame Google, Apple, Microsft, Netflix, Amazon, and Facebook.'},
        {'created_at': 'Oct. 2, 2021, 7:43 p.m.', 'text': '@TMessi_1 @Porkchop_EXP @Cernovich So microsft flight sim is for kids? tell that to the pilots that use it to train.'}
    ]
    df = pd.DataFrame([tweet['text'] for tweet in tweets], columns=["Tweets"])
    df['Tweets'] = df['Tweets'].apply(cleanTxt)
    df["Subjectivity"] = df["Tweets"].apply(getSubjectivity)
    df["Polarity"] = df["Tweets"].apply(getPolarity)
    df["Analysis"] = df["Polarity"].apply(getAnalysis)
    print(df)
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
    # newsapi = NewsApiClient(api_key='bc7e81851ccf4221b6edaf48941a9888')
    # top_headlines = newsapi.get_top_headlines(q='microsoft',
    #                                     sources='bbc-news,the-verge',
    #                                     # category='business',
    #                                     language='en',
    #                                     # country='us'
    #                                     )
    # news = top_headlines
    # print(news)

    news = [{'articles': [{'author': 'Verge Staff',
                'content': 'Come on in, the windows are fine\r\nIf you buy something from a Verge link, Vox Media may earn a commission. See our ethics statement.\r\nMicrosofts next version of Windows, Windows 11, is coming October… [+17914 chars]',
                'description': 'Microsoft’s next version of Windows, Windows 11, is coming October 5th. Technically, a near-final version is already here, and we’ve spent considerable time with it on over a dozen different PCs.',
                'publishedAt': '2021-10-02T15:00:00Z',
                'source': {'id': 'the-verge', 'name': 'The Verge'},
                'title': 'Windows 11 seems okay',
                'url': 'https://www.theverge.com/22705148/windows-11-upgrade-beta-release-preview-impressions',
                'urlToImage': 'https://cdn.vox-cdn.com/thumbor/p_u0ZlnLrGczT6gT7lTppXCub3M=/0x178:2560x1518/fit-in/1200x630/cdn.vox-cdn.com/uploads/chorus_asset/file/22894952/twarren__windows11_sharper.jpg'}],
            'status': 'ok',
            'totalResults': 1},
            {'articles': [{'author': 'Verge Staff',
                'content': 'Come on in, the windows are fine\r\nIf you buy something from a Verge link, Vox Media may earn a commission. See our ethics statement.\r\nMicrosofts next version of Windows, Windows 11, is coming October… [+17914 chars]',
                'description': 'Microsoft’s next version of Windows, Windows 11, is coming October 5th. Technically, a near-final version is already here, and we’ve spent considerable time with it on over a dozen different PCs.',
                'publishedAt': '2021-10-02T15:00:00Z',
                'source': {'id': 'the-verge', 'name': 'The Verge'},
                'title': 'Windows 11 seems okay',
                'url': 'https://www.theverge.com/22705148/windows-11-upgrade-beta-release-preview-impressions',
                'urlToImage': 'https://cdn.vox-cdn.com/thumbor/p_u0ZlnLrGczT6gT7lTppXCub3M=/0x178:2560x1518/fit-in/1200x630/cdn.vox-cdn.com/uploads/chorus_asset/file/22894952/twarren__windows11_sharper.jpg'}],
            'status': 'ok',
            'totalResults': 1}]
    return news
