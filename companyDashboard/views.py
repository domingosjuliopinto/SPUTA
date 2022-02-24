from django.shortcuts import render
from django.contrib import messages
import yfinance 
import tweepy as tw
from tweepy import OAuthHandler
import datetime
from newsapi import NewsApiClient
import datetime

predictions = {'msft': [311.31, 309.1, 305.0, 299.84, 294.31, 288.8, 283.41, 278.02, 272.49, 266.71, 260.74, 254.76, 249.04, 243.87, 239.51, 236.11, 233.75, 232.47, 232.21, 232.94, 234.58, 237.09, 240.39, 244.41, 249.08, 254.29, 259.91, 265.78, 271.71, 277.46],
                'googl': [2585.28, 2539.41, 2431.42, 2294.44, 2151.1, 2020.97, 1919.26, 1852.99, 1820.33, 1812.66, 1817.44, 1820.89, 1810.6, 1777.4, 1716.48, 1627.59, 1515.11, 1387.56, 1256.11, 1131.7, 1022.14, 930.67, 856.26, 795.04, 742.1, 693.02, 645.0, 597.15, 550.27, 506.17],
                'fb': [309.51, 303.5, 294.52, 284.31, 274.25, 265.58, 258.94, 254.33, 251.37, 249.46, 248.0, 246.44, 244.43, 241.79, 238.5, 234.67, 230.52, 226.26, 222.12, 218.25, 214.73, 211.61, 208.84, 206.37, 204.13, 202.06, 200.09, 198.19, 196.33, 194.52],
                'aapl': [137.93, 137.28, 132.8, 125.66, 116.9, 107.26, 97.21, 87.1, 77.21, 67.77, 58.99, 51.05, 44.04, 38.03, 33.01, 28.94, 25.74, 23.3, 21.52, 20.29, 19.52, 19.12, 19.01, 19.12, 19.41, 19.83, 20.34, 20.91, 21.53, 22.16],
                'amzn': [2895.99, 2651.57, 2376.68, 2140.96, 1970.56, 1858.74, 1786.65, 1738.4, 1704.01, 1677.58, 1655.65, 1636.23, 1618.19, 1600.99, 1584.38, 1568.33, 1552.88, 1538.07, 1523.96, 1510.56, 1497.87, 1485.87, 1474.53, 1463.79, 1453.62, 1443.97, 1434.8, 1426.06, 1417.72, 1409.74],
                'nflx': [395.48, 407.78, 405.94, 394.31, 377.83, 360.7, 345.99, 335.27, 328.59, 324.87, 322.66, 320.74, 318.38, 315.22, 311.24, 306.6, 301.54, 296.34, 291.25, 286.47, 282.09, 278.14, 274.59, 271.39, 268.46, 265.73, 263.15, 260.69, 258.34, 256.07]}
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
