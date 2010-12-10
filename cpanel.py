import logging
import string
import wsgiref.handlers
#from google.appengine.ext.webapp import blobstore_handlers
#from google.appengine.ext import blobstore
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from util.sessions import Session
from dbinterface import DataStoreInterface
from stringFormatter import StringFormatter
from emailProcessor import EmailProcessor
from util.twitter_oauth_handler import *
import util.twitter_oauth_handler as twitter_oauth_handler
import util.facebook.__init__ as facebook
from time import time
from bitly import *
import render
 
API_KEY = 'bba630a5c803425bbb00cb137fe0894c'
SECRET_KEY = 'e55f6309bedf9a34a6334a5ccabf7bfe' 

BITLY_USER = 'sstest'
BITLY_KEY = 'R_87f1cbd8d2238c6b626b87be6ba46b79'

class CPanelHandler(webapp.RequestHandler):
	
	def setTwitterAccounts(self, accounts):
		self.twitter = accounts
	
	def get(self):		
		self.session = Session()	
		if 'user' in self.session:
			user = self.session['user']	
			datastore = DataStoreInterface()
		
			formatter = StringFormatter()
			company = formatter.getCompanyProfileName(user)
			email = formatter.getEmail(user)
			
			twitter_oauth_handler.setTwitterAccounts(company)
			twitterAccounts = twitter_oauth_handler.getTwitterAccounts()
			
			facebookAccounts = datastore.getFacebookAccounts(company)
			
			#TWITTER MENTIONS QUERIED			
			mentions = []
			
			for name in twitterAccounts:
				numMention = 0
				client = OAuthClient('twitter', self, name)
				statuses = client.get('/statuses/mentions')
				if statuses == "Could not retrieve from social networks. The server could not be contacted at this time. Please try again later.":
					self.response.out.write(statuses)
					return
				for iteration in statuses:
					numMention += 1
					mention = Mentions()
					mention.dbCreatedTime = iteration['created_at']
					mention.dbMessage = iteration['text']
					mention.dbName = iteration['user']['screen_name']
					mention.dbPostID = str(iteration['id'])
					mention.dbReceiverName = iteration['in_reply_to_screen_name']
					mention.dbLink = 'From: <a href="http://twitter.com/'  + iteration['user']['screen_name']+'" target="_blank">'+ iteration['user']['name'] + '</a>'
					mentions.append(mention)
					if numMention == 5:
						break
		
			comments = []
			
			for name in facebookAccounts:
				fb = facebook.Facebook(API_KEY, SECRET_KEY)
				stream = fb.__call__('Stream.get', {'session_key':name.dbSessionKey, 'source_ids':[name.dbUid], 'limit':5})
				for post in stream['posts']:				
					replies = post['comments']['comment_list']
					numComment = 0
					for reply in replies:
						userInfo = fb.__call__('Users.getInfo', {'session_key':name.dbSessionKey, 'call_id':time(), 'uids':reply['fromid'], 'fields':['first_name', 'last_name']})
						username = userInfo[0]['first_name'] + ' ' + userInfo[0]['last_name']
						status = Comments()
						status.dbUserID = name.dbUid
						status.dbPostID = post['post_id']
						status.dbMessage = reply['text']
						status.dbLink = 'From: <a href="http://www.facebook.com/profile.php?ref=profile&id=' + str(reply['fromid']) + '" target="_blank">' + username + '</a>'
						status.dbReplyTo = 'In reply to: ' + post['message']
						comments.append(status)
						numComment += 1
						if numComment == 3:
							break
					if len(comments) == 10:
						break
						
			#getting saved posts 
			datastore = DataStoreInterface()
			formatter = StringFormatter()
			
			profileName = formatter.getCompanyProfileName(user)
		
			posts = datastore.getSavedPosts(profileName, 25)
			savedPosts = ''
			
			for r in posts:
				savedPosts += formatter.formatSavedPost(r, formatter.formatPost(r, profileName))
			
			#upload_url = blobstore.create_upload_url('/upload')	
			render.doRender(self, 'controlpanel.html', {'user': user, 'mentions': mentions, 'comments':comments, 'savedPosts': savedPosts, 'socialAccounts': twitterAccounts, 'facebookAccounts':facebookAccounts})
		else:
			self.redirect('main.html')
	
	def post (self):
		#intialization of variables
		self.session = Session()
		user = self.session['user']		
		datastore = DataStoreInterface()
		status = ''
		error=''
		message=''
			
		#formatting of user cached account
		formatter = StringFormatter()
		company = formatter.getCompany(user)
		profileName = formatter.getCompanyProfileName(user)
		email = formatter.getEmail(user)
		
		#retrieving content from form fields		
		title = self.request.get('txtTitle')
		id = formatter.formatID(title)
		content = self.request.get('txtContent')
		file = self.request.get("file")
		btnClicked = formatter.getButtonType(self.request.body)
			
		if title<>'':
			
			postLink = ('synapsync.com/update.html?company=%s/id=%s'%(profileName, id))


			bitly = BitLy(BITLY_USER, BITLY_KEY)
			postLink = bitly.shorten(postLink)
			
			#self.response.out.write(postLink)
			#return	

			postAttributes = [company, profileName, email, title, content, id]
			
			#if no file attached then just place type None else use attached file
			if file == '':
				postAttributes.append(None)
			else:
				postAttributes.append(file)
				
			postAttributes.append(postLink)
			
			response = ''
			if (btnClicked == 'Post'):
				status = 'Posted'
				postAttributes.append(status)
				emailObj = EmailProcessor()
			
				
				emails =  []

				emails = datastore.getEmailSubscriber(profileName)
				
				for e in emails:
					if (e <> None and e <> ''):				
						emailObj.sendAnnounceEmail(company, e.strip() , title, content + ' ' + postLink)
			
				#twitter
				#twitterAccounts = datastore.getTwitterAccounts(profileName)
			
				facebookAccounts = datastore.getFacebookAccounts(profileName)
				twitterAccounts = datastore.getTwitterAccounts(profileName)
				twitter = twitterAccounts
				for name in twitter:
					client = OAuthClient('twitter', self, name)
					response = client.post('/statuses/update', status = title + '\n' + postLink)
				for name in facebookAccounts:
					fb = facebook.Facebook(API_KEY, SECRET_KEY)
					fbResponse = fb.__call__('Stream.publish', {'session_key':name.dbSessionKey, 'message':title + '\n' + postLink, 'target_id':name.dbUid, 'uid':name.dbUid})

			elif (btnClicked == 'Save'):
				status = 'Saved'
				postAttributes.append(status)
		
			datastore.putPost(postAttributes)
			
			if response == "SynapSync could not post to Twitter. The server could not be contacted at this time. Please try again later.":
				self.response.out.write(response)
				return
			
		else:
			error = 'Please fill the Title and Content fields below!' 
		self.redirect('controlpanel.html')
		
class Mentions(db.Model):
	dbCreatedTime = db.StringProperty()
	dbMessage = db.TextProperty()
	dbLink = db.StringProperty()
	dbName = db.StringProperty()
	dbPostID = db.StringProperty()
	dbReceiverName = db.StringProperty()
	
class Comments(db.Model):
	dbMessage = db.TextProperty()
	dbLink = db.StringProperty()
	dbReplyTo = db.TextProperty()
	dbName = db.StringProperty()
	dbUserID = db.StringProperty()
	dbPostID = db.StringProperty()