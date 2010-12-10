from dbinterface import DataStoreInterface
from google.appengine.ext import webapp
import render
from emailProcessor import EmailProcessor

class RetrievePassHandler(webapp.RequestHandler):
    def get(self):
        render.doRender(self, 'retrieve.html', {})
    
    def post(self):
	
        email = self.request.get('txtEmail')
        datastore = DataStoreInterface()        
        emailObj = EmailProcessor()
        
        if emailObj.isValidEmail(email) <> 1:
			render.doRender(self, 'retrieve.html', {'error' : 'Invalid email address format!'})
        elif datastore.userExists(email) <> 1:
            render.doRender(self, 'retrieve.html', {'error' : 'Email address has not been registered!'})
        else:
            subject = "SynapSync email password Retrieval for " + email
            password = datastore.getUserPass(email)
            body = """
            Hi,
            
            You are receiving the following email because your password was requested. 
            
            Your info is: 
            
            email: """ + email + """
            password: """ + password + """
            
            Thanks,
            
            SynapSync Team"""
            
            emailObj.sendSupportEmail(email, subject, body) 
            render.doRender(self,'retrieve.html', {'confirmation' : 'Password sent to ' + email})