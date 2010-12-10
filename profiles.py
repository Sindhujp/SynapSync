import logging
import string
import wsgiref.handlers
from google.appengine.api import users
from google.appengine.ext import db
from dbinterface import DataStoreInterface
from stringFormatter import StringFormatter
from google.appengine.ext import webapp
from util.sessions import Session
import render
from datastore import Posts

class ProfilesHandler(webapp.RequestHandler):

	def get(self):
	
		datastore = DataStoreInterface()
		formatter = StringFormatter()
		
		path = self.request.query_string.replace('company=', '')
		posts = datastore.getPosts(path, 25)
		companies = datastore.getCompanyInfo(path) 
		company = datastore.getCompanyName(path)
		
		info=''
		for c in companies:
			info = formatter.formatCompanyInfo(c)
				
		postList=[]
		for p in posts:
			postList.append(formatter.formatPost(p, p.dbProfileName))
		render.doRender(self, 'profiles.html', {'posts': postList, 'company': company , 'info': info, 'profileName' : path})
		
	def post(self):
		datastore = DataStoreInterface()
		email = self.request.get('txtEmail').strip()
		profileName = self.request.query_string.replace('company=', '')
		datastore.addEmailSubscriber(profileName, email)
		
		self.redirect('profiles.html?company='+profileName)
		
class ImageHandler(webapp.RequestHandler):

	def get(self):

		image = db.get(self.request.get("img_id"))
		if image.dbFile:
			self.response.headers['Content-Type'] = 'image/jpeg'
			self.response.out.write(image.dbFile)