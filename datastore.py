#The Synapsync Datastore holds the list of users, posts, and companies in the system.

from google.appengine.ext import db


#The User Model
class Users(db.Model):
    dbEmail = db.StringProperty()
    dbPassword = db.StringProperty()
    dbCompany = db.StringProperty()
    dbFirstName = db.StringProperty()
    dbLastName = db.StringProperty()
    dbPosition = db.StringProperty()
    dbCreatedOn = db.DateProperty(auto_now_add=True)
    dbLastActive = db.DateTimeProperty(auto_now=True)
    
#The User Posts Model
class Posts(db.Model):
    dbCompany = db.StringProperty()
    dbProfileName = db.StringProperty()
    dbEmail = db.StringProperty()
    dbPostDate = db.DateTimeProperty(auto_now_add=True)
    dbLastModified = db.DateTimeProperty(auto_now_add=True)
    dbTitle = db.StringProperty()
    dbBody = db.TextProperty()
    dbFile = db.BlobProperty()
    dbPostState = db.StringProperty()
    dbPostId = db.StringProperty()
    dbShortUrl = db.StringProperty()

#The Companies Model
class Companies(db.Model):
    dbCompanyName = db.StringProperty()
    dbProfileName = db.StringProperty()
    dbPhoneNumber = db.StringProperty()
    dbStreetAddress = db.StringProperty()
    dbCity = db.StringProperty()
    dbState = db.StringProperty()
    dbPostalCode = db.StringProperty()
    dbCountry = db.StringProperty()
    dbUrl = db.StringProperty()
    dbAdministrator = db.StringProperty()
    dbCreatedOn = db.DateProperty(auto_now_add=True)
    dbLastActive = db.DateTimeProperty(auto_now=True)
    dbMailingList = db.TextProperty()
    
#The User Token Model
class UserToken(db.Model):
    dbProfileName = db.StringProperty()
    dbTwitterName = db.StringProperty()
    dbToken = db.StringProperty()
    dbTokenSecret = db.StringProperty()

#Facebook Session
class FbSession(db.Model):
	dbProfileName = db.StringProperty()
	dbSessionKey = db.StringProperty()
	dbUserName = db.StringProperty()
	dbUid = db.StringProperty()