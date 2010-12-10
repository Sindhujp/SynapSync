import logging
import string
import wsgiref.handlers
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.api import mail
from util.sessions import Session
from dbinterface import DataStoreInterface
from emailProcessor import EmailProcessor
import render

class RegisterHandler(webapp.RequestHandler):

  def get(self):
  
    render.doRender(self, 'register.html', {})

  def post(self):
  
    if (self.request.get('txtInviteCode') == 'SYNAPSE'):
        self.session = Session()
        datastore = DataStoreInterface()
    
        #collection of text box contents
        firstName = self.request.get('txtFirstName')
        lastName = self.request.get('txtLastName')
        company = self.request.get('txtCompany')
        email = self.request.get('txtEmail')
        password = self.request.get('txtPass1')
        repassword = self.request.get('txtPass2')
    
        #create session variable 
        self.session.delete_item('user')
        
        #create emailPOrcessor object
        emailObj = EmailProcessor()
                
        #check email address validity
        if emailObj.isValidEmail(email) == 0:
            render.doRender(self, 'register.html', {'error' : 'Invalid email address. Please input a valid email address.'})
            return
    
        #Ensure that the passwords match
        if password <> repassword:
            render.doRender(self, 'register.html', {'error' : 'Password did not match'})
            return
    
        #Check for any fields left empty
        if firstName == '' or lastName == '' or  company == '' or email == '' or password == '' or repassword == '':
            render.doRender(self, 'register.html', {'error' : 'Please fill in all the details'})
            return
    
        #See if the user already exists in the database
        if datastore.userExists(email) == 1:
            render.doRender(self, 'register.html', {'error' : 'The account associated with the email already exists'})
            return
    
        #check if company exists
        #IF it doesn't THEN add user as administrator and create company ELSE add user as editor
        if datastore.companyExists(company) == 0:
            if datastore.addUser([email, password, firstName, lastName, company, 'Administrator']) == 0:
                self.doRender(self, 'register.html', {'error' : 'Database could not add User: Adding a new user requires 6 attributes to be specified.'})
                return
                
            profileName = company.replace(' ', '').lower()
            if datastore.addCompany([company, profileName, email]) == 0:
                self.doRender(self, 'register.html', {'error' : 'Database could not add Company:  Adding a new company requires 3 attributes to be specified.'})
                return
        else:
            if datastore.addUser([email, password, firstName, lastName, company, 'Editor']) == 0:
                self.doRender(self, 'register.html', {'error' : 'Database could not add User: Adding a new user requires 6 attributes to be specified.'})
                return
    
        #create session variable based on email and company name
        username = company + " - " + email
        self.session['user'] = username
        self.redirect('controlpanel.html')
    else:
        render.doRender(self, 'register.html', {'error' : 'Sorry at this time SynapSync is open only to a limited number of users. Please check back at another time. <br><br>Thanks,<br> The SynapSync Team'})