import logging
import cgi
import string
import wsgiref.handlers
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp \
    import template
from util.sessions import Session
import datetime 
from bitly import *

BITLY_USER = 'sstest'
BITLY_KEY = 'R_87f1cbd8d2238c6b626b87be6ba46b79'

class StringFormatter(object):
    
    def formatID(self, title):
        now = datetime.datetime.now()
        title = title.replace(' ', '-')[0:25]
        return title + '-' + now.strftime("%Y-%m-%d-%H-%M") 
        

    def formatText(self, text):    
        return text.replace('+', ' ')
        
    def formatPost(self, post, profileName):
        bitly = BitLy(BITLY_USER, BITLY_KEY)
        postIdLink = 'update.html?company=' + profileName + '/id=' + post.dbPostId
        #shortLink = 'www.synapsync.com/' + postIdLink
        #shortLink = bitly.shorten('www.synapsync.com/' + postIdLink)
        viewCount ='0'		
        if post.dbShortUrl:
        	viewCount = bitly.stats(post.dbShortUrl)
        
        header = '<hr align=left width=100%>' + '<p><b>' + '<a href="' + postIdLink + '">' + post.dbTitle +'</a></b> - <i>' + str(post.dbPostDate) + '</i><br></p>'
        
        body = ('<p>%s</p><p>Viewers: %s</p>'%(post.dbBody, viewCount))
        if post.dbFile:
	        body =('<p>%s<br><img alt="" src="img?img_id=%s"></img></p><p>Viewers: %s</p>'%(post.dbBody,post.key(), viewCount))
		
        return header + body
              
    def formatSavedPost(self, post, formattedPost):
        postActionLink = 'postAction?action=post&id=' + post.dbPostId
        return formattedPost + '<p><b>' + '<a href=' + postActionLink + '">' + 'Post</a></b></p>'
        
    def formatCompanyInfo(self, company):
        companyName = company.dbCompanyName + '<br>' + '<br>'
        contact = str(company.dbStreetAddress) + '<br>' + str(company.dbCity) + ' ' + str(company.dbPostalCode) + '<br>' + str(company.dbState) + ' ' + str(company.dbCountry) + '<br>'
        number = str(company.dbPhoneNumber) + '<br>'
        email = '<a href="contact.html?company='+company.dbProfileName+'">Email</a>' + '<br>'
        url = ('<a href="%s" target="_blank">Website</a>'% str(company.dbUrl))
        
        output = companyName + contact + number + email + url
        
        return output
        

	def formatShortLink(self, attributes):
	    
	    attributes = attributes.split('{')[1]
        
        return attributes
    #Extracts the URL parameter values and returns them in an array
    def getValues(self, parameters):
    
        temp = parameters.split('&')
        values = []
        
        for i in range(0, len(temp)):
        
            attribute = temp[i].split('=')
            values.append(attribute[1])
        
        return values
        
    def getButtonType(self, parameters):
    
        paramValues = self.getValues(parameters)
        return paramValues[len(paramValues) - 1]
        
    def getCompany(self, user):
    
        userInfo = user.split('-')
        return userInfo[0]
        
    def getCompanyProfileName (self, user):
    
        userInfo = user.split('-')
        return userInfo[0].replace(' ', '').lower()
    
    def createID(self, date):
        
        dateID = date.replace('-', '').replace(':', '')
        dateID = dateID[:(dateID.rfind('.'))].strip()
        
        return dateID
        
    
    def getEmail(self, user):
    
        userInfo = user.split('-')
        return userInfo[1].replace(' ', '')