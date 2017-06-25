"""
  ** Author: rlyth
  ** Date: 6/11/17
  ** Description: a RESTful API server for an event planning app
"""


from google.appengine.ext import ndb
import webapp2
import json

	
class Event(ndb.Model):
	id = ndb.StringProperty()
	name = ndb.StringProperty(required=True)
	date = ndb.StringProperty()
	location = ndb.StringProperty()
	host = ndb.StringProperty()
	notes = ndb.TextProperty()
	
class Venue(ndb.Model):
	id = ndb.StringProperty()
	name = ndb.StringProperty(required=True)
	address = ndb.StringProperty()
	phone_num = ndb.IntegerProperty()
	description = ndb.TextProperty()
	max_occupancy = ndb.IntegerProperty()
	event_list = ndb.StringProperty(repeated=True)

	
class EventsHandler(webapp2.RequestHandler):
	def get(self, id=None):
		events = None
		
		# If no ID provided, retrieve list of all events
		if not id:
			events = Event.query().fetch()
		
		basicGet(self, id, events)

	def post(self):
		req = json.loads(self.request.body)
		
		# Check required fields are present and valid
		if 'name' not in req or invalidEventParams(req):
			self.response.set_status(400)
			self.response.write(self.response.status)
			return
		
		# Create event
		parent_key = ndb.Key(Event, "parent_event")
		new_entry = Event(name=req['name'], parent=parent_key)
		new_entry.put()
		
		new_entry.id = new_entry.key.urlsafe()
		
		# Optional parameters
		if 'date' in req:
			new_entry.date = req['date']
		if 'location' in req:
			new_entry.location = req['location']
		if 'host' in req:
			new_entry.host = req['host']
		if 'notes' in req:
			new_entry.notes = req['notes']
		
		# Update database
		new_entry.put()
		
		self.response.set_status(201)
		d = new_entry.to_dict()
		self.response.write(json.dumps(d))
			
	def patch(self, id=None):
		if id:
			req = json.loads(self.request.body)
			
			# Attempt to retrieve event
			event = getByKey(id)
				
			# Not a valid event
			if event is None:
				self.response.set_status(404)
				self.response.write(self.response.status)
				return

			# Invalid number
			if invalidEventParams(req):
				self.response.set_status(400)
				self.response.write(self.response.status)
				return

			# Update provided values
			if 'name' in req:
				event.name = req['name']
			if 'date' in req:
				event.date = req['date']
			if 'location' in req:
				event.location = req['location']
			if 'host' in req:
				event.host = req['host']
			if 'notes' in req:
				event.notes = req['notes']	
			
			# Update database
			event.put()
			
			# Return updated event to user
			self.response.set_status(200)
			d = event.to_dict()
			self.response.write(json.dumps(d))
		else:
			self.response.set_status(403)
			self.response.write(self.response.status)
			
	def delete(self, id=None):
		if id:
			# Attempt to retrieve event
			event = getByKey(id)
			
			# Not a valid event
			if event is None:
				self.response.set_status(404)
				self.response.write(self.response.status)
				return
		
			# Remove event from all venues
			venues = Venue.query().fetch()
			for v in venues:
				if id in v.event_list:
					v.event_list.remove(id)
					v.put()
		
			# Delete event
			ndb.Key(urlsafe=id).delete()
			
			self.response.set_status(204)
			self.response.write(self.response.status)
		else:
			self.response.set_status(403)
			self.response.write(self.response.status)
			
			
class VenueHandler(webapp2.RequestHandler):
	def get(self, id=None):
		venues = None;
		
		# If no id, get list of all entries
		if not id:
			venues = Venue.query().fetch()
			
		basicGet(self, id, venues)
		
	def post(self, id=None):
		req = json.loads(self.request.body)
		
		# Check required fields are present and valid
		if 'name' not in req or invalidVenueParams(req):
			self.response.set_status(400)
			self.response.write(self.response.status)
			return
		
		# Create new entry
		parent_key = ndb.Key(Venue, "parent_venue")
		new_entry = Venue(name=req['name'], parent=parent_key)
		new_entry.put()
		
		new_entry.id = new_entry.key.urlsafe()
		
		# Optional parameters
		if 'max_occupancy' in req:
			new_entry.max_occupancy = req['max_occupancy']
		if 'address' in req:
			new_entry.address = req['address']
		if 'phone_num' in req:
			new_entry.phone_num = req['phone_num']
		if 'description' in req:
			new_entry.description = req['description']
		if 'event_list' in req:
			new_entry.event_list = req['event_list']
		
		# Update database
		new_entry.put()
		
		self.response.set_status(201)
		d = new_entry.to_dict()
		self.response.write(json.dumps(d))
		
	def patch(self, id=None):
		if id:
			req = json.loads(self.request.body)
			
			# Retrieve entry
			entry = getByKey(id)
				
			# Not a valid id
			if entry is None:
				self.response.set_status(404)
				self.response.write(self.response.status)
				return

			# Invalid parameters
			if invalidVenueParams(req):
				self.response.set_status(400)
				self.response.write(self.response.status)
				return

			# Update provided values
			if 'name' in req:
				entry.name = req['name']
			if 'max_occupancy' in req:
				entry.max_occupancy = req['max_occupancy']
			if 'address' in req:
				entry.address = req['address']
			if 'phone_num' in req:
				entry.phone_num = req['phone_num']
			if 'description' in req:
				entry.description = req['description']
			
			# Update database
			entry.put()
			
			# Return updated entry to user
			self.response.set_status(200)
			d = entry.to_dict()
			self.response.write(json.dumps(d))
		else:
			self.response.set_status(403)
			self.response.write(self.response.status)
		
	def delete(self, id=None):
		if id:
			# Attempt to retrieve entry
			entry = getByKey(id)
			
			# No entry with that id exists
			if entry is None:
				self.response.set_status(404)
				self.response.write(self.response.status)
				return
		
			# Delete entry
			ndb.Key(urlsafe=id).delete()
			
			self.response.set_status(204)
			self.response.write(self.response.status)
		else:
			self.response.set_status(403)
			self.response.write(self.response.status)
			
			
class VenueEventHandler(webapp2.RequestHandler):
	def put(self, id=None):
		if id:
			req = json.loads(self.request.body)
			
			venue = getByKey(id)
			
			# Check if venue exists
			if venue is None:
				self.response.set_status(404)
				self.response.write(self.response.status)
				return
			
			# Check if event id was included
			if 'event_id' not in req:
				self.response.set_status(400)
				self.response.write(self.response.status)
				return
				
			# Attempt to retrieve event
			event = getByKey(req['event_id'])
			
			# Check that event exists
			if event is None:
				self.response.set_status(404)
				self.response.write(self.response.status)
				return
			
			# Reject if duplicate
			if event.id in venue.event_list:
				self.response.set_status(403)
				self.response.write(self.response.status)
				return
			
			# Proceed to add event to event list
			venue.event_list.append(req['event_id'])
			
			venue.put()
			
			self.response.set_status(200)
			d = venue.to_dict()
			self.response.write(json.dumps(d))
		else:
			self.response.set_status(403)
			self.response.write(self.response.status)

	def get(self, id=None):
		if id:
			venue = getByKey(id)
	
			# Check if venue exists
			if venue is None:
				self.response.set_status(404)
				self.response.write(self.response.status)
				return
	
			# Retrieve all events from list
			eventList = []
			for e in venue.event_list:
				event = getByKey(e)
				
				if event:
					d = event.to_dict()
					eventList.append(d)
				else:
					# Clean up any dead event ids
					venue.event_list.remove(e)
			
			self.response.set_status(200)
			self.response.write(json.dumps(eventList))
		else:
			self.response.set_status(403)
			self.response.write(self.response.status)
	
	def delete(self, id=None, ev=None):
		if id and ev:
			venue = getByKey(id)
			
			# Check if venue exists
			if venue is None:
				self.response.set_status(404)
				self.response.write(self.response.status)
				return
				
			event = getByKey(ev)
			
			# Check that event exists
			if event is None:
				self.response.set_status(404)
				self.response.write(self.response.status)
				return
				
			# Event not in event_list
			if ev not in venue.event_list:
				self.response.set_status(403)
				self.response.write(self.response.status)
				return
				
			# Update venue
			venue.event_list.remove(ev)
			
			venue.put()
		
			self.response.set_status(200)
			d = venue.to_dict()
			self.response.write(json.dumps(d))
		else:
			self.response.set_status(403)
			self.response.write(self.response.status)
	
	def post(self, id=None):
		self.response.set_status(403)
		self.response.write(self.response.status)
		
		
####################
# Helper functions #
####################

def isNumber(testVal):
	if type(testVal) is int or type(testVal) is float:
		return True
	return False
	
	
def invalidEventParams(req):
	# Check that name is provided and valid
	if 'name' in req and type(req['name']) is not unicode:
		return True
	
	# Check optional fields are valid if provided
	if 'host' in req and type(req['host']) is not unicode:
		return True
	
	if 'location' in req and type(req['location']) is not unicode:
		return True
	
	return False
	
	
def invalidVenueParams(req):
	if 'name' in req and type(req['name']) is not unicode:
		return True
		
	if 'max_occupancy' in req and type(req['max_occupancy']) is not int:
		return True
	
	return False
	
	
def getByKey(safeKey):
	# Returns object from db OR None if doesn't exist
	try:
		thing = ndb.Key(urlsafe=safeKey).get()
	except:
		return None
	
	return thing
	
# Returns a specific item if id is provided or a list of items otherwise
def basicGet(self, id, things):
	if id:
		# Attempt to retrieve
		thing = getByKey(id)

		# Not valid
		if thing is None:
			self.response.set_status(404)
			self.response.write(self.response.status)
			return

		# Return thing
		self.response.set_status(200)
		d = thing.to_dict()
		self.response.write(json.dumps(d))
	else:
		# Return info from all items in things
		tList = []
		for t in things:
			newThing = t.to_dict()
			tList.append(newThing)
			
		self.response.set_status(200)
		self.response.write(json.dumps(tList))
	
	
class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write("Event Coordinator API")

		
# enables Patch method
allowed_methods = webapp2.WSGIApplication.allowed_methods
new_allowed_methods = allowed_methods.union(('PATCH',))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods
		
		
app = webapp2.WSGIApplication([
    ('/', MainPage),
	('/event', EventsHandler),
	('/event/', EventsHandler),
	('/event/(.*)', EventsHandler),
	('/venue/(.*)/event/(.*)', VenueEventHandler),
	('/venue/(.*)/event', VenueEventHandler),
	('/venue', VenueHandler),
	('/venue/(.*)', VenueHandler),
], debug=True)