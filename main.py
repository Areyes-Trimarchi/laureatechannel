import webapp2
import json
from apiclient.discovery import build
from apiclient.errors import HttpError

class RequestPage(webapp2.RequestHandler):
	def get(self):
		self.error(404)
class JsonHandler(webapp2.RequestHandler):
	def get(self):
		pass

app = webapp2.WSGIApplication([
	webapp2.Route('/request', handler = RequestPage, name = 'request'),webapp2.Route('/json', handler = JsonHandler, name = 'json')
	],debug=True)

query = JsonHandler().get('query', default_value = None)

if query and len(query)>=2:
	query_result = perform_youtube_query(query)
else:
	query_result = []


