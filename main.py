import webapp2
import json
import urllib
import cgi

DEVELOPER_KEY = "AIzaSyAFM-ucrRbBBI8HYaf5Lk08tYLpjaBya34"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
CHANNEL_ID = "UCvS6-K6Ydmb4gH-kim3AmjA"

class MainHandler(webapp2.RequestHandler):
  def get(self):
      self.response.out.write("""
          <html>
            <body>
              <p>Alvaro Reyes</p>
              <form action="/retrieve_allvids" method="post">
                <p>Devolver todos los videos del canal</p>
                <div><input type="submit" value="Retrieve"></div>
              </form>
              <form action="/search_by_name" method="post">
                <p>Busqueda por Nombre del video</p>
                <div><textarea name="nombrevid" rows="1" cols="60"></textarea></div>
                <div><input type="submit" value="Buscar"></div>
              </form>
              <form action="/search_by_desc" method="post">
                <p>Busqueda por la descripcion del video</p>
                <div><textarea name="description" rows="1" cols="60"></textarea></div>
                <div><input type="submit" value="Buscar"></div>
              </form>
            </body>
          </html>""")
      
class Laureate_allVids(webapp2.RequestHandler):
  def post(self):
    search_response = urllib.urlopen("https://www.googleapis.com/"+YOUTUBE_API_SERVICE_NAME+"/"+YOUTUBE_API_VERSION+"/search?key="+DEVELOPER_KEY+"&channelId="+CHANNEL_ID+"&part=snippet,id&order=title&maxResults=50")
    json_data = json.loads(search_response.read())
    pageInfo = json_data['pageInfo']
    count = pageInfo['totalResults']
    contador = 0
    for x in range(1,count/50):
      contador = contador + 1
      print(contador)
      next_page = json_data['nextPageToken']
      search_response = urllib.urlopen("https://www.googleapis.com/"+YOUTUBE_API_SERVICE_NAME+"/"+YOUTUBE_API_VERSION+"/search?pageToken="+next_page+"&key="+DEVELOPER_KEY+"&channelId="+CHANNEL_ID+"&part=snippet,id&order=title&maxResults=50")
      json_data_2 = json.loads(search_response.read())
      items=json_data_2['items']
      json_data['items'].extend(items)
    json_data = json.dumps(json_data, sort_keys=True, indent=4, separators=(',', ': '))
    self.response.write(json_data)
    
class Laureate_get_byTitle(webapp2.RequestHandler):
  def post(self):
    search_response = urllib.urlopen("https://www.googleapis.com/"+YOUTUBE_API_SERVICE_NAME+"/"+YOUTUBE_API_VERSION+"/search?key="+DEVELOPER_KEY+"&channelId="+CHANNEL_ID+"&part=snippet,id&order=title&maxResults=50")
    json_data = json.loads(search_response.read())
    pageInfo = json_data['pageInfo']
    count = pageInfo['totalResults']
    videoId = ""
    title = cgi.escape(self.request.get('nombrevid'))
    contador=0
    if title != "":
      items=json_data['items']
      for data_comparison in items:
            if title in data_comparison['snippet']['title']:
              videoId = data_comparison['id']['videoId']
              break
      for x in range(1,count/50):
        contador = contador + 1
        print(contador)
        if videoId == "":
          next_page = json_data['nextPageToken']
          search_response = urllib.urlopen("https://www.googleapis.com/"+YOUTUBE_API_SERVICE_NAME+"/"+YOUTUBE_API_VERSION+"/search?pageToken="+next_page+"&key="+DEVELOPER_KEY+"&channelId="+CHANNEL_ID+"&part=snippet,id&order=title&maxResults=50")
          json_data = json.loads(search_response.read())
          items=json_data['items']
          for data_comparison in items:
            if title in data_comparison['snippet']['title']:
              videoId = data_comparison['id']['videoId']
              break
        else:
          break
      if videoId == "":
        self.response.write("No se encontro ningun video con ese nombre")
      else:
        search_response_vid = urllib.urlopen("https://www.googleapis.com/"+YOUTUBE_API_SERVICE_NAME+"/"+YOUTUBE_API_VERSION+"/videos?key="+DEVELOPER_KEY+"&id="+videoId+"&part=snippet,id&order=date&maxResults=20")
        json_data_vid = json.loads(search_response_vid.read())
        json_data_vids = json.dumps(json_data_vid, sort_keys=True, indent=4, separators=(',', ': '))
        self.response.write(json_data_vids)
    else:
      self.response.write("usted dejo el valor de titulo en blanco")
      
class Laureate_get_byDesc(webapp2.RequestHandler):    
  def post(self):
    search_response = urllib.urlopen("https://www.googleapis.com/"+YOUTUBE_API_SERVICE_NAME+"/"+YOUTUBE_API_VERSION+"/search?key="+DEVELOPER_KEY+"&channelId="+CHANNEL_ID+"&part=snippet,id&order=title&maxResults=50")
    json_data = json.loads(search_response.read())
    pageInfo = json_data['pageInfo']
    count = pageInfo['totalResults']
    videoId = ""
    description = cgi.escape(self.request.get('description'))
    contador=0
    if description != "":
      items=json_data['items']
      for data_comparison in items:
            if description in data_comparison['snippet']['description']:
              videoId = data_comparison['id']['videoId']
              break
      for x in range(1,count/50):
        contador = contador + 1
        print(contador)
        if videoId == "":
          next_page = json_data['nextPageToken']
          search_response = urllib.urlopen("https://www.googleapis.com/"+YOUTUBE_API_SERVICE_NAME+"/"+YOUTUBE_API_VERSION+"/search?pageToken="+next_page+"&key="+DEVELOPER_KEY+"&channelId="+CHANNEL_ID+"&part=snippet,id&order=title&maxResults=50")
          json_data = json.loads(search_response.read())
          items=json_data['items']
          for data_comparison in items:
            if description in data_comparison['snippet']['description']:
              videoId = data_comparison['id']['videoId']
              break
        else:
          break
      if videoId == "":
        self.response.write("No se encontro ningun video con esa descripcion")
      else:
        search_response_vid = urllib.urlopen("https://www.googleapis.com/"+YOUTUBE_API_SERVICE_NAME+"/"+YOUTUBE_API_VERSION+"/videos?key="+DEVELOPER_KEY+"&id="+videoId+"&part=snippet,id&order=date&maxResults=20")
        json_data_vid = json.loads(search_response_vid.read())
        json_data_vids = json.dumps(json_data_vid, sort_keys=True, indent=4, separators=(',', ': '))
        self.response.write(json_data_vids)
    else:
      self.response.write("usted dejo el valor de descripcion en blanco")
      

application = webapp2.WSGIApplication([('/',MainHandler),
                                       ('/search_by_name', Laureate_get_byTitle),
                                       ('/search_by_desc', Laureate_get_byDesc),
                                       ('/retrieve_allvids', Laureate_allVids)
                                      ],debug = True)

def main():
    from paste import httpserver
    httpserver.serve(application, host='127.0.0.1', port='8040')

if __name__ == '__main__':
    main()
