import webapp2

class RequestPage(webapp2.RequestHandler):
	def get(self):
		self.response.out.write('Hola dundo')

application = webapp2.WSGIApplication([('/',RequestPage)
	],debug=True)
