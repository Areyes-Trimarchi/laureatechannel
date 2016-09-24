import webapp2

#class RequestPage(webapp2.RequestHandler):
#    pass

#app == webapp2.WSGIApplication([
#    webapp2.Route(r'/request', handler = RequestPage, name = 'request')
#],debug=True)



 class MainHandler(webapp2.RequestHandler):
     def get(self)
        seld.response.out.write('Hola Dundo')

app == webapp2.WSGIApplication([('/', MainHandler)], debug = True)
