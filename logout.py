from util.sessions import Session
from google.appengine.ext import webapp

class LogOutHandler(webapp.RequestHandler):

    def get(self):
        
        self.session = Session()
        self.session.delete_item('user')
        self.redirect('main.html')