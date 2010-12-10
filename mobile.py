import wsgiref.handlers
from dbinterface import DataStoreInterface
from google.appengine.ext import webapp
from stringFormatter import StringFormatter

class MobileHandler(webapp.RequestHandler):
    def get(self):
        formatter = StringFormatter()
        datastore = DataStoreInterface()
        
        queries = []
        queries = formatter.getValues(self.request.query_string)
        
        if len(queries) == 1:
            if (datastore.companyProfileExists(queries[0]) == 1):                
                posts = datastore.getPosts(queries[0], 5)
                
                for p in posts:
                    self.response.out.write(p.dbTitle + ' - ' + p.dbBody + '<br>')
            else:
                self.response.out.write('Company Not Found')
    
        else:
            self.response.out.write("unknown query")