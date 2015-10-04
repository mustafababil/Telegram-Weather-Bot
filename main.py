# -*- coding: utf-8 -*-

import StringIO
import json
import logging
import random
import urllib
import urllib2

# Custom imports
from inputModel import inputModel
import responseController
#import create_db

# for sending images
from PIL import Image
import multipart

# standard app engine imports
from google.appengine.api import urlfetch
from google.appengine.ext import ndb
import webapp2


######## GLOBAL VARIABLES ########

TOKEN = '58737283:AAGB3v1c27r_rgsur5nCfc53gndhKg9iR_8'

BASE_URL = 'https://api.telegram.org/bot' + TOKEN + '/'

WEATHER_BASE_URL = 'http://api.openweathermap.org/data/2.5/weather?'
WEATHER_API_KEY = '04f9cff3a5fbb8c457e31444bae05328'
WEATHER_CITY_NAME = 'q='
WEATHER_CITY_LAT = 'lat='
WEATHER_CITY_LNG = 'lon='
WEATHER_UNIT = 'metric'
WEATHER_DAY_CNT = 1

degree_sign= u'\N{DEGREE SIGN}'



# ================================


######## HELPER CLASSES AND FUNCTIONS ########

class EnableStatus(ndb.Model):
    # key name: str(chat_id)
    enabled = ndb.BooleanProperty(indexed=False, default=False)


# ================================

def setEnabled(chat_id, yes):
    es = EnableStatus.get_or_insert(str(chat_id))
    es.enabled = yes
    es.put()

def getEnabled(chat_id):
    es = EnableStatus.get_by_id(str(chat_id))
    if es:
        return es.enabled
    return False

# ================================

class MeHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'getMe'))))


class GetUpdatesHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'getUpdates'))))


class SetWebhookHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        url = self.request.get('url')
        if url:
            self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'setWebhook', urllib.urlencode({'url': url})))))


######## MAIN BOT WORK DONE HERE ########

class WebhookHandler(webapp2.RequestHandler):

    def post(self):
        urlfetch.set_default_fetch_deadline(60)
        body = json.loads(self.request.body)
        
        # Console Log input message from user
        logging.info('request body:')
        logging.info(json.dumps(body))  # escape " u' " from input
        

        """
            Fetch user input
        """
        self.response.write(json.dumps(body))       # QUESTION: What does response() do exactly?
        newInput = inputModel(body)     # Initialize input model with user input

        update_id = newInput.getUpdateID()
        message_id = newInput.getMessageID()
        text = newInput.getText()
        fromID = newInput.getFromID()
        fromUserName = newInput.getFromName()
        chat_id = newInput.getChatID()
        location = newInput.getLocation()
        lat = newInput.getLat()
        lng = newInput.getLng()



        if text or location:    # check if text or location is entered
            if text:            # for text inputs
                if text.startswith('/'):    # check if command
                    if text.lower() == '/start':
                        responseController.sendTextMessage(chat_id, '@Weathercast_Bot started\nPlease enter the city name as \'text\' or send as \'location\'\nComing features:\n Forecast for next day(s)\n Daily notification \n\n->City,Country\n->Location')
                        setEnabled(chat_id, True)

                    elif text.lower() == '/stop':
                        responseController.sendTextMessage(chat_id, 'Bot disabled')
                        setEnabled(chat_id, False)

                    elif text.lower() == '/help':
                        responseController.sendTextMessage(chat_id, 'Write as city,country or just send your location easily')

                    elif text.lower().startswith('/weather'):
                        responseController.sendTextMessage(chat_id, 'Please enter city name or send location coordinates directly')
                        
                    else:
                        responseController.sendTextMessage(chat_id, 'Enter from available commands')
                        return
                

                else:           # text is not command, it is brief text
                    if getEnabled(chat_id):
                        weatherResponse = responseController.textInputRequest(text)     # Make request to weather API and get results
                        responseController.textInputHandler(chat_id, weatherResponse)   # Handle response
                        return                                                          # finish process

                    else:
                        logging.info('not enabled for chat_id {}'.format(chat_id))
                        responseController.sendTextMessage(chat_id, 'Please enable bot by writing /start')


                return
            else:               # for location inputs
                weatherResponse = responseController.locationInputRequest(lat, lng)     # Make request to weather API and get results
                responseController.locationInputHandler(chat_id, weatherResponse)       # Handle response
                return                                                                  # finish process

        else:                   # no meaningful input, EXIT!
            logging.info('no text or location from user')
            responseController.sendTextMessage(chat_id, 'Enter your location by text or map')
            return


app = webapp2.WSGIApplication([
    ('/me', MeHandler),
    ('/updates', GetUpdatesHandler),
    ('/set_webhook', SetWebhookHandler),
    ('/webhook', WebhookHandler),
], debug=True)
