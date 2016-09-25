import webapp2
import json
import urllib

DEVELOPER_KEY = "AIzaSyBiORXw-clppwKozQSbmZqydDMK0UDL6xk"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
CHANNEL_ID = "UCvS6-K6Ydmb4gH-kim3AmjA"

class MainHandler(webapp2.RequestHandler):
  def get(self):
    search_response = urllib.urlopen("https://www.googleapis.com/"+YOUTUBE_API_SERVICE_NAME+"/"+YOUTUBE_API_VERSION+"/search?key="+DEVELOPER_KEY+"&channelId="+CHANNEL_ID+"&part=snippet,id&order=date&maxResults=20")
    data = {}
    data['response']= search_response.read()
    json_data = json.dumps(data)
    self.response.write("Hi there")
    self.response.write(json_data)
    print(json_data)

  def youtube_search(self,title,description):
    search_response = urllib.urlopen("https://www.googleapis.com/"+YOUTUBE_API_SERVICE_NAME+"/"+YOUTUBE_API_VERSION+"/search?key="+DEVELOPER_KEY+"&channelId="+CHANNEL_ID+"&part=snippet,id&order=date&maxResults=20")
    data = {}
    data['response']= search_response.read()
    json_data = json.dumps(data)
    self.response("Hi there")
    print(json_data)

application = webapp2.WSGIApplication([('/',MainHandler),
                              ],debug = True)


