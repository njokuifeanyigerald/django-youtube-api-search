from django.shortcuts import render, redirect
import requests
from isodate import parse_duration
from django.conf import settings
# Create your views here.
def home(request):
    videos = []
    if request.method == 'POST':
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'
        params =  {
            "part": "snippet",
            'q': request.POST['q'],
            'key': settings.YOUTUBE_DATA_API,
            'maxResults': 9,
            'type': 'video'
        }
        video_ids = []
        r = requests.get(search_url, params=params)
        results = r.json()['items']

        for result in results:
            video_ids.append(result['id']['videoId'])
        if request.POST['button'] == "youtube":
            return redirect(f'https:www.youtube.com/watch?v={video_ids[0]}')
        video_params= {
            'part': 'snippet, contentDetails',
            'key': settings.YOUTUBE_DATA_API,
            'id': ','.join(video_ids)
        }
        r = requests.get(video_url, params=video_params)
        results = r.json()['items']
        for result in results:
            video_data  = {
                'title': result['snippet']['title'],
                'id': result['id'],
                'url': f'https:www.youtube.com/watch?v={result["id"]}',
                'duration': int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
                'thumbnail': result['snippet']['thumbnails']['high']['url']
            }
            videos.append(video_data)
    context = {
        "videos":videos
    }
    return render(request, 'home.html', context)