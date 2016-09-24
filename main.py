import webapp2
import json

class RequestPage(webapp2.RequestHandler):
    def get(self):
        #self.error(404)
        self.response.write('hi there')
#class JsonHandler(webapp2.RequestHandler):
    #def get(self):
    #    pass
app == webapp2.WSGIApplication([
    webapp2.Route('/request', handler = RequestPage, name = 'request'),
    #webapp2.Route('/json/?', handler = JsonHandler, name = 'json')
],debug=True)
