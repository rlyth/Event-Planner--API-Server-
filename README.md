# Event Planner (API Server)
A simple API backend hosted on Google App Engine, to be used with the Event Planner mobile app.

### Reference
**POST /event/**
<br>Creates a new event using the provided parameters.

**Parameters**
> name, string (required)
> <br>date, string
> <br>location, string
> <br>host, string
> <br>notes, string

**GET /event/**
<br>Returns data from all events.
 
**GET /event/{event_id}**
<br>Returns data from the event whose id is provided.
 
**PATCH /event/{event_id}**
<br>Edits any editable parameters of event whose id is provided.

**Parameters**
> name, string
> <br>date, string
> <br>location, string
> <br>host, string
> <br>notes, string

**DELETE /event/{event_id}**
<br>Deletes the event whose id is provided. If the event was assigned to any venues, it is removed from the event_list of those venues.
 
**POST /venue/**
<br>Creates a new venue using the provided parameters.

**Parameters**
> name, string (required)
> <br>address, string
> <br>phone_num, int
> <br>max_occupancy, int
> <br>description, string

**GET /venue/**
<br>Returns data from all venues.
 
**GET /venue/{venue_id}**
<br>Returns data from the venue whose id is provided.
 
**PATCH /venue/{venue_id}**
<br>Edits any editable parameters of venue whose id is provided.

**Parameters**
> name, string
> <br>address, string
> <br>phone_num, int
> <br>max_occupancy, int
> <br>description, string

**DELETE /venue/{venue_id}**
<br>Deletes the venue whose id was provided. This does NOT delete events associated with this venue.
 
**PUT /venue/{venue_id}/event**
<br>If not already in Venue.event_list for the venue whose id is provided, the event id provided in the request body will be added to Venue.event_list for this venue.

**Parameters**
> event_id, string (required)

**GET /venue/{venue_id}/event**
<br>Returns an array of events for all events whose keys are in Venue.event_list for the venue whose id is provided.
 
**DELETE /venue/{venue_id}/event/{event_id}**
<br>If the venue whose id is provided has in their Venue.event_list the id of the event whose id is provided, the event is removed from the venue’s event_list.
