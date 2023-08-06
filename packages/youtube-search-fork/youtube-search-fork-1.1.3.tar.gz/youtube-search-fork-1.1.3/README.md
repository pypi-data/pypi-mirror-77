# youtube_search-fork
This fork adds the ability to search for channels, latest content of a channel and adds videos published date.

Python function for searching for youtube videos to avoid using their heavily rate-limited API

To avoid using the API, this uses the form on the youtube homepage and scrapes the resulting page.

## Installation
`pip install youtube-search-fork`

## Example Usage
For a basic search (and all of the current functionality), you can use the search tool as follows:

```python
from youtube_search import YoutubeSearch

videos = YoutubeSearch('search terms', max_results=10).videos_to_json()
channels = YoutubeSearch('search terms', max_results=10).channels_to_json()

print(results)

# returns a json string

########################################

videos = YoutubeSearch('search terms', max_results=10).videos_to_dict()
channels = YoutubeSearch('search terms', max_results=10).channels_to_dict()

print(results)
# returns a dictionary like this:
[{'id': 'UCJWCJC...CieLOLQ', 'name': 'channelName', 'suscriberCountText': '200.000', 'thumbnails': ['URL1', 'URL2'], 'url_suffix': '/user/channelName'}]

```
