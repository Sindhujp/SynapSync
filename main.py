import logging
import string
import wsgiref.handlers
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp \
    import template
from util.sessions import Session
from dbinterface import DataStoreInterface
from profiles import *
from register import RegisterHandler
from cpanel import *
from settings import SettingsHandler
from retrievepass import RetrievePassHandler
from twittercallback import TwitterCallbackHandler
from update import UpdateHandler
from fbauth import *
from logout import LogOutHandler
from mobile import MobileHandler
from contact import ContactHandler
from testEmail import EmailHandler
from reply import *
from postAction import postActionHandler
from util.twitter_oauth_handler import *
from dbinterface import *
import render


class MainHandler(webapp.RequestHandler):

	def get(self):
	
		path = (self.request.path).replace('/', '')
		datastore = DataStoreInterface()
		
		if (path <> '') and (path <> 'main.html'):
			if (datastore.companyProfileExists(path) == 1):				
				path = 'profiles.html?company='+path
				self.redirect(path)
			else:
				self.response.out.write('404: File not Found')
		else:
			render.doRender(self,'main.html', {})
	
	def post(self):
		
		self.session = Session()
		datastore = DataStoreInterface()
		
		email = self.request.get('txtEmail').strip()
		password = self.request.get('txtPassword')
		
		self.session.delete_item('user')
		
		#Check for any fields left empty
		if email == '' or password == '':
			render.doRender(self, 'main.html', {'error' : 'Please fill in all the details'})
			return
		
		username = datastore.loginUser(email, password)
		
		if datastore.isUser(email)== 1:
			if datastore.checkPass(email, password)==1:	
				self.session['user'] = username			
				self.redirect('controlpanel.html')
			else:
				render.doRender(self, 'main.html', {'error' : 'Wrong password'})
		else:
			render.doRender(self, 'main.html', {'error' : 'Email Address does not exist'})

def main():
  application = webapp.WSGIApplication([('/facebook/', FbAuthHandler),
										('/facebook/callback/', FbCallbackHandler),
										('/fbauthorized/.*', FbSessionHandler),
                                        ('/register.html', RegisterHandler),
										('/controlpanel.html', CPanelHandler),
										('/profiles.html', ProfilesHandler),
										('/settings.html', SettingsHandler),
										('/retrieve.html', RetrievePassHandler),                                        
                                        ('/update.html', UpdateHandler),
                                        ('/mobile', MobileHandler),
                                        ('/contact.html', ContactHandler),
                                        ('/postAction', postActionHandler),
										('/twitter_oauth', TwitterCallbackHandler),
										('/twitter_reply.*', TwitterReplyHandler),
										('/facebook_reply.*', FacebookReplyHandler),
										('/oauth/(.*)/(.*)', OAuthHandler),
                                        ('/logout', LogOutHandler),
                                        ('/email', EmailHandler),
                                        ('/img', ImageHandler),
										('/.*', MainHandler)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
