from django.shortcuts import render
from django.contrib import messages
import yfinance 
import tweepy as tw
from tweepy import OAuthHandler
import datetime
from newsapi import NewsApiClient
import datetime

predictions = {'msft':[311.31, 309.1, 305.0, 299.84, 294.31, 288.8, 283.41, 278.02, 272.49, 266.71, 260.74, 254.76, 249.04, 243.87, 239.51, 236.11, 233.75, 232.47, 232.21, 232.94, 234.58, 237.09, 240.39, 244.41, 249.08, 254.29, 259.91, 265.78, 271.71, 277.46],
                'googl':[]}
# Create your views here.
def dashboard(request):
<<<<<<< HEAD
    listedCompany = ['NASDAQ:MSFT', 'NASDAQ:GOOGL', 'NASDAQ:FB', 'NASDAQ:AAPL']
=======
    listedCompany = ['NASDAQ:MSFT', 'NASDAQ:GOOGL', 'NASDAQ:FB', 'NASDAQ:APPL']
>>>>>>> 0f1b4ef5314f0d29d49f2806b1a0198f245aa751
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
                # prediction = predictions[int(str(datetime.date.today()).split("-")[2]) - 1]
                companyPrediction = predictions[ticker.split(':')[1].lower()]
                prediction = companyPrediction[int(str(datetime.date.today()).split("-")[2]) - 1]
                context = {
                    'ticker': ticker,
                    'url1': url1,
                    'url2': url2,
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
