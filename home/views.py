from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
# from apiclient.discovery import build

# Create your views here.
def home(request):
    # api_key = ""
    # youtube = build('youtube', 'v3', developerKey = api_key)
    # req = youtube.search().list(q="stocks market", part = 'snippet', type = "video")
    # res = req.execute()
    res = {'kind': 'youtube#searchListResponse', 'etag': 'wz1fdMewo_FU4_12IDYzNHrVjN0', 'nextPageToken': 'CAUQAA', 'regionCode': 'IN', 'pageInfo': {'totalResults': 1000000, 'resultsPerPage': 5}, 'items': [{'kind': 'youtube#searchResult', 'etag': 'eYr9YaQ_MEDVURTBBticrSuX71Q', 'id': {'kind': 
'youtube#video', 'videoId': 'SHEXYL9At8M'}, 'snippet': {'publishedAt': '2022-05-04T08:35:25Z', 'channelId': 'UCGa9XVjGTrQPDZ_OeV65tug', 'title': '😱3 Major reasons why Market down today🔴Why stock market crash today 🔴why share market down today', 'description': 'Major reasons why Market down today  Why stock market crash today us bond yield news  Why market is falling today | why ...', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/SHEXYL9At8M/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/SHEXYL9At8M/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/SHEXYL9At8M/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'Be Wise & Wealthy', 'liveBroadcastContent': 'none', 'publishTime': '2022-05-04T08:35:25Z'}}, {'kind': 'youtubesearchResult', 'etag': 'dgZk2TvGv74CwlXzrNahy3u2sOM', 'id': {'kind': 'youtubevideo', 'videoId': 'Xn7KWR9EOGQ'}, 'snippet': {'publishedAt': '2019-02-12T12:58:15Z', 'channelId': 'UCe3qdG0A_gr-sEdat5y2twQ', 'title': 'Basics of Stock Market For Beginners  Lecture 1 By CA Rachana Phadke Ranade', 'description': "You can get my Stock Market courses on https://www.rachanaranade.com It's an opportunity to learn 65+ concepts relating to the ...", 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/Xn7KWR9EOGQ/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/Xn7KWR9EOGQ/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/Xn7KWR9EOGQ/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'CA Rachana Phadke Ranade', 'liveBroadcastContent': 'none', 'publishTime': '2019-02-12T12:58:15Z'}}, {'kind': 'youtubesearchResult', 'etag': 'DZkVHYvklRmHayVK2nXGCXYn6e0', 'id': {'kind': 'youtubevideo', 'videoId': 'VBPeumOEkq8'}, 'snippet': {'publishedAt': '2022-05-03T13:15:01Z', 'channelId': 'UCSglJMvX-zSgv3PEJIE_inw', 'title': 'Top Dividend Stocks in Falling Stock Market', 'description': 'NEW! Sign Up for DCF Calculator Website & Community Access: https://bit.ly/3daErcc Robinhood Sign Up: ...', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/VBPeumOEkq8/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/VBPeumOEkq8/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/VBPeumOEkq8/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'Learn to Invest', 'liveBroadcastContent': 'none', 'publishTime': '2022-05-03T13:15:01Z'}}, {'kind': 'youtubesearchResult', 'etag': 'gZnOxlj1libVOO5guPHcUNDIEmU', 'id': {'kind': 'youtubevideo', 'videoId': 'ZCFkWDdmXG8'}, 'snippet': {'publishedAt': '2020-04-17T13:00:02Z', 'channelId': 'UCWOA1ZGywLbqmigxE4Qlvuw', 'title': 'Explained | The Stock Market | FULL EPISODE | Netflix', 'description': 'In partnership with Vox Media Studios and Vox, this enlightening explainer series will take viewers deep inside a wide range of ...', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/ZCFkWDdmXG8/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/ZCFkWDdmXG8/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/ZCFkWDdmXG8/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'Netflix', 'liveBroadcastContent': 'none', 'publishTime': '2020-04-17T13:00:02Z'}}, {'kind': 'youtubesearchResult', 'etag': '6N59eVu8qXkobo34LqGfEZYmCeg', 'id': {'kind': 'youtubevideo', 'videoId': '-NOAjwJvt9A'}, 'snippet': {'publishedAt': '2022-05-03T21:04:27Z', 'channelId': 'UCmlfS56nZsnX_5F1fjvX0QA', 'title': 'Is A Bigger Stock Market CRASH Coming? How To Trade The Trend &amp; Momentum In A Bull &amp; Bear Market PT1', 'description': 'Thank you for taking the time to watch. If you want to support these videos, you can do so by following this link. Tips and Donations ...', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/-NOAjwJvt9A/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/-NOAjwJvt9A/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/-NOAjwJvt9A/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'Ron Walker', 'liveBroadcastContent': 'none', 'publishTime': '2022-05-03T21:04:27Z'}}]}
    videos = []
    thumbnails= []
    for vid in res['items']:
        print(vid['id']['videoId'])
        # urlVideo = "https://www.googleapis.com/youtube/v3/videos?part=snippet&id=" + vid['id']['videoId'] + '"=AIzaSyA3Fg-1Qaz3Ula4M2FTBOFoEMrcxCPB-rI"'
        urlVideo = "https://youtu.be/" + vid['id']['videoId']
        videos.append(urlVideo)
    for thumbnail in res['items']:
        print(thumbnail)
        thumbnails.append(thumbnail['snippet']['thumbnails']['high']['url'])
    # https://www.googleapis.com/youtube/v3/videos?part=snippet&id=xE_rMj35BIM&key="AIzaSyA3Fg-1Qaz3Ula4M2FTBOFoEMrcxCPB-rI"
    return render(request, 'home/base.html', {"res": res['items'], "videosthumb": zip(videos, thumbnails)})

def loginUser(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect('/')
        else:
            messages.error(request, "Wrong Credentials")
            return render(request, 'home/login.html')
    else: 
        return render(request, 'home/login.html')
    
def logoutUser(request):
    logout(request)
    messages.success(request, "successfully logged out")
    return redirect('/')