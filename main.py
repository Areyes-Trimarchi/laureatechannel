import webapp2
import json
import urllib

DEVELOPER_KEY = "AIzaSyAFM-ucrRbBBI8HYaf5Lk08tYLpjaBya34"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
CHANNEL_ID = "UCvS6-K6Ydmb4gH-kim3AmjA"

class MainHandler(webapp2.RequestHandler):
  def get(self,title,description):
    search_response = urllib.urlopen("https://www.googleapis.com/"+YOUTUBE_API_SERVICE_NAME+"/"+YOUTUBE_API_VERSION+"/search?key="+DEVELOPER_KEY+"&channelId="+CHANNEL_ID+"&part=snippet,id&order=date&maxResults=20")
    json_data = json.loads(search_response.read())
    items=json_data['items']
    videoId = ""
    for data_comparison in items:
      if title in data_comparison['snippet']['title'] or description in data_comparison['snippet']['description']:
        videoId = data_comparison['id']['videoId']
        break

    search_response_vid = urllib.urlopen("https://www.googleapis.com/"+YOUTUBE_API_SERVICE_NAME+"/"+YOUTUBE_API_VERSION+"/videos?key="+DEVELOPER_KEY+"&id="+videoId+"&part=snippet,id&order=date&maxResults=20")
    json_data = json.loads(search_response_vid.read())
    print(json_data)
    

application = webapp2.WSGIApplication([('/',MainHandler),
                              ],debug = True)

application.run()
main = MainHandler()
main.get("Robotic Contest 2016 Animation","")
