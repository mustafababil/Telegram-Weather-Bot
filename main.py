# -*- coding: utf-8 -*-

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

WEATHER_BASE_URL = 'http://api.openweathermap.org/data/2.5/weather?'
WEATHER_API_KEY = '04f9cff3a5fbb8c457e31444bae05328'
WEATHER_CITY_NAME = 'q='
WEATHER_CITY_LAT = 'lat='
WEATHER_CITY_LNG = 'lon='
WEATHER_UNIT = 'metric'
WEATHER_DAY_CNT = 1

degree_sign= u'\N{DEGREE SIGN}'

thunderstorm = u'\U0001F4A8'    # Code: 200's, 900, 901, 902, 905
drizzle = u'\U0001F4A7'         # Code: 300's
rain = u'\U00002614'            # Code: 500's
snowflake = u'\U00002744'       # Code: 600's snowflake
snowman = u'\U000026C4'         # Code: 600's snowman, 903, 906
atmosphere = u'\U0001F301'      # Code: 700's foogy
clearSky = u'\U00002600'        # Code: 800 clear sky
fewClouds = u'\U000026C5'       # Code: 801 sun behind clouds
clouds = u'\U00002601'          # Code: 802-803-804 clouds general
hot = u'\U0001F525'             # Code: 904



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
        if text:
            text = text.encode('utf-8','strict')

        fr = message.get('from')        # get from object, includes username, first_name, last_name, id keys
        userID  = fr['id']              # get User ID
        first_name = fr['first_name']   # get User first name

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
                logging.debug('Input text: ' + str(text))
                resp = urllib.urlopen(BASE_URL + 'sendMessage', urllib.urlencode({
                    'chat_id': str(chat_id),
                    'text': msg.encode('utf-8','strict')
                })).read()
            elif img:
                resp = multipart.post_multipart(BASE_URL + 'sendPhoto', [
                    ('chat_id', str(chat_id)),
                    ('reply_to_message_id', str(message_id)),
                ], [
                    ('photo', 'image.jpg', img),
                ])
            else:
                ('no msg or img specified')
                resp = None

            logging.info('send response:')
            logging.info(resp)


        """
            Return related emojis according to weather
        """
        def getEmoji(weatherID):
            if weatherID:
                if str(weatherID)[0] == '2' or weatherID == 900 or weatherID==901 or weatherID==902 or weatherID==905:
                    return thunderstorm
                elif str(weatherID)[0] == '3':
                    return drizzle
                elif str(weatherID)[0] == '5':
                    return rain
                elif str(weatherID)[0] == '6' or weatherID==903 or weatherID== 906:
                    return snowflake + ' ' + snowman
                elif str(weatherID)[0] == '7':
                    return atmosphere
                elif weatherID == 800:
                    return clearSky
                elif weatherID == 801:
                    return fewClouds
                elif weatherID==802 or weatherID==803 or weatherID==803:
                    return clouds
                elif weatherID == 904:
                    return hot
                else:
                    return u'\U0001F300'    # Default emoji

            else:
                return u'\U0001F300'    # Default emoji

        if text or location:    # check if text or location is entered
            if text:            # for text inputs
                if text.startswith('/'):    # check if command
                    if text.lower() == '/start':
                        reply('Weathercast_Bot started\nPlease enter the city name as \'text\' or send as \'location\' \n\n->City,Country\n->Location')
                        setEnabled(chat_id, True)

                    elif text.lower() == '/stop':
                        reply('Bot disabled')
                        setEnabled(chat_id, False)

                    elif text.lower() == '/help':
                        reply('Write the as follows city,country or just easily send your location')

                    elif text.lower().startswith() == '/weather':
                        reply('Please enter city name or send location coordinates')

                    else:
                        #reply('Enter command?')
                        return
                else:           # text is not command, it is brief text
                    if getEnabled(chat_id):
                        #WEATHER_URL_TEXT = WEATHER_BASE_URL + WEATHER_CITY_NAME + text + '&APPID=' + WEATHER_API_KEY + '&units=' + WEATHER_UNIT + '&cnt=' + str(WEATHER_DAY_CNT) 
                        #WEATHER_URL_TEXT = urllib.quote_plus(WEATHER_URL_TEXT)
                        #
                        
                        urlEncodePairs = { 'q': text, 'APPID': WEATHER_API_KEY, 'units': WEATHER_UNIT, 'cnt': 1 }
                        encodedURL = urllib.urlencode(urlEncodePairs)

                        WEATHER_URL_TEXT = WEATHER_BASE_URL + encodedURL
                        logging.debug("REQ URL: " + WEATHER_URL_TEXT)

                        weatherResponse = json.load(urllib2.urlopen(WEATHER_URL_TEXT))

                        resultCode = weatherResponse.get('cod')

                        if resultCode == 200:       # Success city find
                            cityName = weatherResponse.get('name')
                            countryName = weatherResponse.get('sys').get('country')
                            temp_current = weatherResponse.get('main').get('temp')
                            temp_max = weatherResponse.get('main').get('temp_max')
                            temp_min = weatherResponse.get('main').get('temp_min')
                            description = weatherResponse.get('weather')[0].get('description')
                            description_brief = weatherResponse.get('weather')[0].get('main')
                            
                            weatherID = weatherResponse.get('weather')[0].get('id')     # gets ID of weather description, used for emoji
                            emoji = getEmoji(weatherID)
                            
                            reply(cityName + ', ' + countryName + ': ' + str(temp_current) + degree_sign + 'C\n' +
                                'Max temp: ' + str(temp_max) + degree_sign + 'C - ' + 'Min temp: ' + str(temp_min)+ degree_sign  + 'C\n' +
                                'Description: ' + description_brief + ' - ' + description + emoji)
                            
                        else:       # Not found city
                            errorCode = weatherResponse.get('message')
                            reply(str(resultCode) + ' - ' + errorCode)
                        
                        return  # finish process
                    else:
                        logging.info('not enabled for chat_id {}'.format(chat_id))
                return
            else:               # for location inputs
                WEATHER_URL_COORD = WEATHER_BASE_URL + WEATHER_CITY_LAT + str(lat) + '&' + WEATHER_CITY_LNG + str(lng) + '&APPID=' + WEATHER_API_KEY + '&units=' + WEATHER_UNIT + '&cnt=' + str(WEATHER_DAY_CNT) 
                weatherResponse = json.load(urllib2.urlopen(WEATHER_URL_COORD))

                resultCode = weatherResponse.get('cod')
                if resultCode == 200:   # Success city found
                    cityName = weatherResponse.get('name')
                    countryName = weatherResponse.get('sys').get('country')
                    temp_current = weatherResponse.get('main').get('temp')
                    temp_max = weatherResponse.get('main').get('temp_max')
                    temp_min = weatherResponse.get('main').get('temp_min')
                    description = weatherResponse.get('weather')[0].get('description')
                    description_brief = weatherResponse.get('weather')[0].get('main')

                    weatherID = weatherResponse.get('weather')[0].get('id')     # gets ID of weather description, used for emoji
                    emoji = getEmoji(weatherID)

                    reply(cityName + ', ' + countryName + ': ' + str(temp_current) + degree_sign + 'C\n' +
                                'Max temp: ' + str(temp_max) + degree_sign + 'C - ' + 'Min temp: ' + str(temp_min) + degree_sign + 'C\n' +
                                'Description: ' + description_brief + ' - ' + description + emoji)

                else:       # Not found city
                    errorCode = weatherResponse.get('message')
                    reply(str(resultCode) + ' - ' + errorCode)

                return          # finish process
        else:                   # no meaningful input, EXIT!
            logging.info('no text or location from user')
            #reply('Enter your location by text or map')
            return


app = webapp2.WSGIApplication([
    ('/me', MeHandler),
    ('/updates', GetUpdatesHandler),
    ('/set_webhook', SetWebhookHandler),
    ('/webhook', WebhookHandler),
], debug=True)
