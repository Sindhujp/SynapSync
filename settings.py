from google.appengine.ext import webapp
from util.sessions import Session
from dbinterface import DataStoreInterface
from stringFormatter import StringFormatter
import render

class SettingsHandler(webapp.RequestHandler):

	def get(self):
		self.session = Session()

		if 'user' in self.session:
			formatter = StringFormatter()
			user = self.session['user']	
			company = formatter.getCompanyProfileName(user)
			email = formatter.getEmail(user)

			datastore = DataStoreInterface()
			twitterAccounts = datastore.getTwitterAccounts(company)
			facebookAccounts = datastore.getFacebookAccounts(company)
			
			uInfo = datastore.getUserInfo(email)
			
			for u in uInfo:
				firstName = u.dbFirstName 
				lastName = u.dbLastName
				
				
			
			cInfo = datastore.getCompanyInfo(company)
			
			for c in cInfo:
				cname = c.dbCompanyName
				stAddress = c.dbStreetAddress
				city = c.dbCity
				state = c.dbState
				zip = c.dbPostalCode
				country = c.dbCountry
				number = c.dbPhoneNumber
				cemail = c.dbAdministrator
				website = c.dbUrl

			if datastore.isAdmin(company, email) == 1:
				render.doRender(self, 'settings.html', {'isAdmin':email,'email':email,'firstName':firstName, 'lastName':lastName, 'socialAccounts' : twitterAccounts
													    ,'facebookAccounts':facebookAccounts, 'cname':cname, 'stAddress':stAddress, 'city':city, 'state':state, 'zip':zip
													    ,'country':country, 'number':number, 'cemail':cemail, 'website':website })
			else:
				render.doRender(self, 'settings.html', {'email':email})
		else:
			render.doRender(self, 'main.html', {})
	
	def post(self):
	
		datastore = DataStoreInterface()
		
		email = self.request.get('txtEmail')
		first = self.request.get('txtFirstName')
		last = self.request.get('txtLastName')
		#password code should go here
		company = self.request.get('txtCompanyName')
		street = self.request.get('txtStreetAddress')
		city = self.request.get('txtCity')
		state = self.request.get('txtState')
		zip = self.request.get('txtZip')
		country = self.request.get('txtCountry')
		phone = self.request.get('txtPhoneNumber')
		site = self.request.get('txtWebsite')
		
		#self.response.out.write(company)
		
		userAttributes = [first, last]
		companyAttributes = [company, street, city, state, zip, country, phone, site]
		
		if ((datastore.changeCompanyInfo(company, companyAttributes)) and (datastore.changeUserInfo(email, userAttributes))):
			render.doRender(self, 'controlpanel.html', {'message':'Changed Information'})
		else:
			render.doRender(self, 'settings.html', {'error':'Could not change in database'})

		