import StringIO
import json
import logging
import random
import urllib
import urllib2

# for sending images
from PIL import Image
import multipart

# standard app engine imports
from google.appengine.api import urlfetch
from google.appengine.ext import ndb
import webapp2

TOKEN = '58737283:AAGB3v1c27r_rgsur5nCfc53gndhKg9iR_8'

BASE_URL = 'https://api.telegram.org/bot' + TOKEN + '/'


# ================================

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


class WebhookHandler(webapp2.RequestHandler):

    def post(self):
        urlfetch.set_default_fetch_deadline(60)
        body = json.loads(self.request.body)
        
        # Console Log input message from user
        logging.info('request body:')
        logging.info(json.dumps(body))

        """
            Fetch some types from user input
        """
        self.response.write(json.dumps(body))

        update_id = body['update_id']   # get update_id

        message = body['message']       # get message object
        message_id = message.get('message_id')  # get message_id
        date = message.get('date')      # get date
        text = message.get('text')      # get user input text

        fr = message.get('from')        # get from object, includes username, first_name, last_name, id keys

        chat = message['chat']          # get chat object, includes username, first_name, last_name, id keys
        chat_id = chat['id']            # get chat_id

        location = message.get('location')  # get location object
        if location:
            lat = location['latitude']  # get latitude
            lng = location['longitude'] # get longitude

        """
            To send message or image to user
        """
        def reply(msg=None, img=None):
            if msg:
                resp = urllib2.urlopen(BASE_URL + 'sendMessage', urllib.urlencode({
                    'chat_id': str(chat_id),
                    'text': msg.encode('utf-8'),
                    'disable_web_page_preview': 'true'
                })).read()
            elif img:
                resp = multipart.post_multipart(BASE_URL + 'sendPhoto', [
                    ('chat_id', str(chat_id)),
                    ('reply_to_message_id', str(message_id)),
                ], [
                    ('photo', 'image.jpg', img),
                ])
            else:
                logging.error('no msg or img specified')
                resp = None

            logging.info('send response:')
            logging.info(resp)


        if text or location:    # check if text or location is entered
            if text:            # for text inputs
                if text.startswith('/'):    # check if command
                    if text.lower() == '/start':
                        reply('Weathercast_Bot enabled\nPlease enter the city name as \'text\' or send as \'location\'')
                        setEnabled(chat_id, True)

                    elif text.lower() == '/stop':
                        reply('Bot disabled')
                        setEnabled(chat_id, False)

                    else:
                        reply('Enter command?')
                else:           # text is not command
                    if getEnabled(chat_id):
                        # TODO: hava durumu command
                        reply('text but not command')
                    else:
                        logging.info('not enabled for chat_id {}'.format(chat_id))
                return
            else:               # for location inputs
                reply('entered location')
                return
        else:                   # no meaningful input, EXIT!
            logging.info('no text or location from user')
            reply('Enter your location by text or map')
            return


app = webapp2.WSGIApplication([
    ('/me', MeHandler),
    ('/updates', GetUpdatesHandler),
    ('/set_webhook', SetWebhookHandler),
    ('/webhook', WebhookHandler),
], debug=True)
