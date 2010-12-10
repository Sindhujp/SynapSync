from datastore import *
from stringFormatter import StringFormatter
from google.appengine.api import images

class DataStoreInterface(object):

    #USER CALLS
    def userExists(self, email):
    
        query = db.Query(Users)
        query = query.filter('dbEmail =', email)
        results = query.fetch(limit = 1)
        
        if len(results) > 0 :
            return 1
        return 0
        
    def addUser(self, userAttributes):
    
        if len(userAttributes) <> 6:
            return 0
    
        newUser = Users(dbEmail = userAttributes[0], dbPassword = userAttributes[1], dbFirstName = userAttributes[2], dbLastName = userAttributes[3], dbCompany = userAttributes[4], dbPosition = userAttributes[5])
        newUser.put();
        return 1
    
    def changeUserInfo(self, email, userAttributes):
    	if self.isUser(email):
    		query = db.Query(Users)
    		query = query.filter('dbEmail =', email)
    		results = query.fetch(limit=1)
    		
    		
    		for r in results:
    			#r.dbPassword = 
			    r.dbFirstName = userAttributes[0] 
			    r.dbLastName = userAttributes[1]
			    r.put()
			    return 1	
		else:
			return 0
			        
    def isUser(self, email):
        query = db.Query(Users)
        query = query.filter('dbEmail =', email)
        results = query.fetch(limit = 1)
        
        if len(results) == 0:
            return 0;
        else:
            return 1;
        
    def checkPass(self, email, password):
        if password == self.getUserPass(email):
            return 1;
        else:
            return 0;
        
        
    def loginUser(self, email, password):    
        query = db.Query(Users)
        query = query.filter('dbEmail =', email)
        query = query.filter('dbPassword =', password)
        results = query.fetch(limit = 1)
        
        username = ''
        if len(results) > 0:
            for p in results:
                name = p.dbCompany
                username = name + " - " + email
        return username
    
    def getAdminEmail(self, company):
        query = db.Query(Companies)
        query = query.filter('dbProfileName =', company)
        results = query.fetch(limit = 1)
        
        email = 'null'
        for r in results:
            email = r.dbAdministrator
                        
        return email
    
    #checks if given email address belongs to an admin account of the given company
    def isAdmin(self, companyProfile, email):
        query = db.Query(Companies)
        query = query.filter('dbProfileName =', companyProfile)
        results = query.fetch(limit = 1)
        admin=''
        
        for r in results:
            admin = r.dbAdministrator
            
        if email == admin:
            return 1
        else:
            return 0
    
    def getUserPass(self, email):
        
        query = db.Query(Users)
        query = query.filter('dbEmail =', email)
        results = query.fetch(limit = 1)
        
        for r in results:
            return r.dbPassword

    #returns a list of twitter accounts registered to the companyProfile
    def getTwitterAccounts(self, companyProfile):
                
        query = db.Query(UserToken)
        query = query.filter('dbProfileName =', companyProfile)
        results = query.fetch(limit = 5)
        
        socialAccounts = []
        for r in results:
            socialAccounts.append(r.dbTwitterName)
            
        return socialAccounts
            
    def getFacebookAccounts(self, companyProfile):
	
        query = db.Query(FbSession)
        query = query.filter('dbProfileName =', companyProfile)
        results = query.fetch(limit = 5)
        
        socialAccounts = []
        for r in results:
            socialAccounts.append(r)
            
        return socialAccounts
	
    def getUserInfo(self, email):
        
        query = db.Query(Users)
        query = query.filter('dbEmail =', email)
        
        return query.fetch(limit = 1)
    
    #COMPANY CALLS
    def companyExists(self, company):

        query = db.Query(Companies)
        query = query.filter('dbCompanyName =', company)
        results = query.fetch(limit = 1)
        
        if len(results) > 0 :
            return 1
        return 0
    
    def companyProfileExists(self, companyProfile):

        query = db.Query(Companies)
        query = query.filter('dbProfileName =', companyProfile)
        results = query.fetch(limit = 1)
        
        if len(results) > 0 :
            return 1
        return 0
        
    def addCompany(self, companyAttributes):
    
        if len(companyAttributes) <> 3:
            return 0

        newCompany = Companies(dbCompanyName = companyAttributes[0], dbProfileName = companyAttributes[1], dbAdministrator = companyAttributes[2])
        newCompany.put();
        return 1
        
    def getCompanyInfo(self, profileName):
    
        query = db.Query(Companies)
        query.filter('dbProfileName =', profileName)
        results = query.fetch(1)
        
        return results
        
    def getCompanyName(self, profileName):
        query = db.Query(Companies)
        query.filter('dbProfileName =', profileName)
        results = query.fetch(1)
        
        company=''
        
        for c in results:
            company = c.dbCompanyName
        
        return company
    def addEmailSubscriber(self, profileName, email):
        query = db.Query(Companies)
        query.filter('dbProfileName = ', profileName)
        results = query.fetch(1)
        
        email+=','
        
        for r in results:
            if (r.dbMailingList <> None):
                old = r.dbMailingList
                r.dbMailingList = old + email
            else:
                r.dbMailingList = email
        r.put()
        return
    
    def getEmailSubscriber(self, profileName):
        emails = []
        
        query = db.Query(Companies)
        query.filter('dbProfileName =', profileName)
        results = query.fetch(1)
        
        for r in results:
        	if r.dbMailingList <> None:
	            emails = r.dbMailingList.split(',')
            
        return emails
        
    def changeCompanyInfo(self, company, companyAttributes):
        		    
		if self.companyExists(company):	    
			query = db.Query(Companies)
			query = query.filter('dbCompanyName =', companyAttributes[0])
			results = query.fetch(limit=1)
			
			for r in results:
				r.dbStreetAddress = companyAttributes[1]
				r.dbCity = companyAttributes[2]
				r.dbState = companyAttributes[3]
				r.dbPostalCode = companyAttributes[4]
				r.dbCountry = companyAttributes[5]
				r.dbPhoneNumber = companyAttributes[6]
				r.dbUrl = companyAttributes[7]
				r.put()
				return 1
			return 0
		else:
			return 0

    #POST CALLS
    def getPosts(self, profileName, numResults):
    
        query = db.Query(Posts)
        query.filter('dbProfileName =', profileName).filter('dbPostState =', 'Posted')
        query.order('-dbPostDate')
        results = query.fetch(limit = numResults)
                        
        return results
    
    def getPost(self, profileName, id):
        query = db.Query(Posts)
        query.filter('dbProfileName =', profileName).filter('dbPostState =', 'Posted').filter('dbPostId =', id)
        results = query.fetch(limit = 1)

        return results
    
    def getSavedPosts(self, profileName, numResults):
        query = db.Query(Posts)
        query.filter('dbProfileName =', profileName).filter('dbPostState =', 'Saved')
        query.order('-dbPostDate')
        results = query.fetch(limit = numResults)
        return results
    
    def putPost(self, postAttributes):
    	
        #return postAttributes[7]

        newPost = Posts()

        newPost.dbCompany = postAttributes[0]
        newPost.dbProfileName= postAttributes[1]
        newPost.dbEmail= postAttributes[2]
        newPost.dbTitle= postAttributes[3]
        newPost.dbBody= postAttributes[4]
        newPost.dbPostId= postAttributes[5]
        if postAttributes[6] <> None:
            newPost.dbFile= db.Blob(images.resize(postAttributes[6],200,200))
            #newPost.dbFile= db.Blob(postAttributes[6])

        newPost.dbShortUrl= postAttributes[7]
        newPost.dbPostState= postAttributes[8]
        newPost.put()
        
    def changePostStatus(self, postId, Status):
        
        query = db.Query(Posts)
        query.filter('dbPostId = ', postId)
        results = query.fetch(limit = 1)
        ctr = 0
        for r in results:
            if r.dbPostId == postId:
                ctr=ctr+1
            r.dbPostState = 'Posted'
            
        r.put()
        
        return ctr
    
    #SOCIAL CALLS    
    def getUserToken(self, twitterName=''):
    
        query = db.Query(UserToken)
        query.filter('dbTwitterName =', twitterName)
        results = query.fetch(1)
        token = None
        
        for t in results:
            token = t
        
        return token