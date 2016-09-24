import webapp2
import os
import jinja2

from google.appengine.api import users

template_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.getcwd()))

class RequestPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        login_url = users.create_login_url(self.request.path)
        logout_url = users.create_logout_url(self.request.path)

        template = template_env.get_template('home.html')
        context = {
            'user': user,
            'login_url': login_url,
            'logout_url': logout_url,
        }
        self.response.out.write(template.render(context))

application = webapp2.WSGIApplication([('/',RequestPage)],
                                        debug=True)
