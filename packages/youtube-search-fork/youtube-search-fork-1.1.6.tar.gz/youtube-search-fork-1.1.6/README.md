# youtube_search-fork
This fork adds the ability to search for channels, latest content of a channel, channel information, channel vidoes, and adds videos published date and channelId.
It works scrapping the Youtube pages.

- [x] Search on youtube avoiding the use their heavily rate-limited API. 
- [x] No need for Google account.
- [x] No limits.
- [x] Reasonably fast.

## Installation
`pip install youtube-search-fork`

## Example Usage
For a basic search (and all of the current functionality), you can use the search tool as follows:

1. Get Youtube channel videos and channel info and parse it to JSON.
```python
from youtube_search import YoutubeSearch

videos = YoutubeSearch('search terms', max_results=10).videos_to_json()
channels = YoutubeSearch('search terms', max_results=10).channels_to_json()

print(results)
```
This will print all the info in a JSON format.


2. Get Youtube search videos and channels and parse it to a dict.
```python
from youtube_search import YoutubeSearch

videos = YoutubeSearch('search terms', max_results=10).videos_to_dict()
channels = YoutubeSearch('search terms', max_results=10).channels_to_dict()
print(results)
```

This will print a dictionary like this:
```[{'id': 'UCJWCJC...CieLOLQ', 'name': 'channelName', 'suscriberCountText': '200.000', 'thumbnails': ['URL1', 'URL2'], 'url_suffix': '/user/channelName'}]```


3. Get a specific channel info and videos:
```python
from youtube_search import YoutubeSearch
data = YoutubeSearch.channelInfo(channel_id)


channelInfo = data[0]
channelVideoList = data[1]
```
You will get all the data of the requested channel on `channelInfo`:
```{'id': 'UCjr2bPAyPV.....8Q', 'name': 'Channel Name', 'avatar': 'https://yt3.ggpht.com/a/AATXAJzuPoT_2M54dus-P2qXgnbY0MPxbkzvwv3muxQn=s176-c-k-c0x00ffffff-no-rj', 'subCount': '24K'}```

And all the found videos on `channelVideoList`:
```[{'videoTitle': 'Video title goes here', 'id': 'video_id_here', 'channelName': 'Channel Name', 'timeStamp': '17 hours ago', 'views': '13,661 views', 'videoThumb': 'https://i.ytimg.com/vi/3eC4Hp4MNBA/hqdefault.jpg?sqp=-oaymwEiCKgBEF5IWvKriqkDFQgBFQAAAAAYASUAAMhCPQCAokN4AQ==&rs=AOn4....5o_2mazZd40g_xc_3917M5w', 'channelUrl': '/channel/UCjr2bPA.......gT3W8Q'}, {...}, {...}, ...]```


4. You can request **only** the channel info:
```python
from youtube_search import YoutubeSearch

# The second (and optional) parameter is `includeVideos`. By default is se to True.
channelOnlyData = YoutubeSearch.channelInfo(channel_id, False)
channelInfo = data[0]
```
