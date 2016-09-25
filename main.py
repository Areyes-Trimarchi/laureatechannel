import webapp2
import json
import urllib

DEVELOPER_KEY = "AIzaSyAFM-ucrRbBBI8HYaf5Lk08tYLpjaBya34"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
CHANNEL_ID = "UCvS6-K6Ydmb4gH-kim3AmjA"

class MainHandler(webapp2.RequestHandler):
  def get(self):
    pass
  def youtube_search(self,title,description):
    search_response = urllib.urlopen("https://www.googleapis.com/"+YOUTUBE_API_SERVICE_NAME+"/"+YOUTUBE_API_VERSION+"/search?key="+DEVELOPER_KEY+"&title="+title+"&description="+description+"&channelId="+CHANNEL_ID+"&part=snippet,id&order=date&maxResults=20")
    data = {}
    data['response']= search_response.read()
    json_data = json.dumps(data)
    print(json_data)

main = MainHandler()
main.youtube_search("Robotics","")
app = webapp2.WSGIApplication([('/',MainHandler),
                              ],debug = True)
