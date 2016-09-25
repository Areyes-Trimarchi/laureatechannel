import webapp2
import json
from apiclient.discovery import build

class MainHandler(webapp2.RequestHandler):
  DEVELOPER_KEY = "AIzaSyBmjjEjlr2FfvxyTX4OR6Ljgk_WkvWTcPw"
  YOUTUBE_API_SERVICE_NAME = "youtube"
  YOUTUBE_API_VERSION = "v3"

  def youtube_search(options):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

    search_response = youtube.search().list(
      q = options.q,
      part = "id,snippet",
      maxResults = 50,
    ).execute()

    videos = []
    channels = []
    playlists = []

    for search_result in search_response.get("items", []):
      if search_result["id"]["kind"] == "youtube#video":
        videos.append("%s (%s)" % (search_result["snippet"]["title"],
                                  search_result["id"]["videoId"]))
      if search_result["id"]["kind"] == "youtube#channel":
        channels.append("%s (%s)" % (search_result["snippet"]["title"],
                                  search_result["id"]["channelId"]))
      if search_result["id"]["kind"] == "youtube#playlist":
        playlists.append("%s (%s)" % (search_result["snippet"]["title"],
                                  search_result["id"]["playlistId"]))

    print "Videos:\n", "\n".join(videos), "\n"
    print "Channels:\n", "\n".join(channels), "\n"
    print "Playlists:\n", "\n".join(playlists), "\n"

if __name__ == "__main__":
  argparser.add_argument("--q", help="Search term", default="Google")
  argparser.add_argument("--max-results", help="Max results", default=25)
  args = argparser.parse_args()

  try:
    youtube_search(args)
  except HttpError, e:
    print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)

app = webapp2.WSGIApplication([('/',MainHandler),
                              ],debug = True)