import os
import logging
import string
import wsgiref.handlers
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp \
    import template
from util.sessions import Session


def doRender(handler, tname = 'main.html', values = { }):
	temp = os.path.join(
		os.path.dirname(__file__),
		'templates/' + tname)
	if not os.path.isfile(temp):
		return False
	# Make a copy of the dictionary 
	newval = dict(values)
	newval['path'] = handler.request.path
	handler.session = Session()
	if 'user' in handler.session:
		newval['user'] = handler.session['user']
	outstr = template.render(temp, newval)
	handler.response.out.write(outstr)
	# handler.request.get(outstr)
	return True