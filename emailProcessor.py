from google.appengine.api import mail


class EmailProcessor(object):
    
    def isValidEmail(self, email):
        if not mail.is_email_valid(email):
            return 0;
        else:
            return 1;
        
    def sendSupportEmail(self, recipient, subject, body):
        
        sender = "SynapSync Support <support@synapsync.com>"        
        mail.send_mail(sender, recipient, subject, body) 
        
    def sendAnnounceEmail(self, companyName,  recipient, subject, body):
        #something here
        sender = companyName + " <announce@synapsync.com>"        
        mail.send_mail(sender, recipient, subject, body)