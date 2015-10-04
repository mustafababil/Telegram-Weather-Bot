
import urllib
import urllib2
import json
import StringIO

# standard app engine imports
import logging

# Openweathermap Weather codes and corressponding emojis
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
defaultEmoji = u'\U0001F300'    # default emojis

###

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

################################################

"""
    Handles location inputs.
    Parses Openweathermap @response and sends the information to user at specified @chat_id
"""
def locationInputHandler(chat_id, response):
    resultCode = response.get('cod')

    if resultCode == 200:   # Success city found
        cityName = response.get('name')
        countryName = response.get('sys').get('country')
        temp_current = response.get('main').get('temp')
        temp_max = response.get('main').get('temp_max')
        temp_min = response.get('main').get('temp_min')
        description = response.get('weather')[0].get('description')
        description_brief = response.get('weather')[0].get('main')

        weatherID = response.get('weather')[0].get('id')     # gets ID of weather description, used for emoji
        emoji = getEmoji(weatherID)

        message = cityName + ', ' + countryName + ': ' + str(temp_current) + degree_sign + 'C\n' + 'Max: ' + str(temp_max) + degree_sign + 'C - ' + 'Min: ' + str(temp_min) + degree_sign + 'C\n' + description_brief + ' - ' + description + emoji + emoji

        sendTextMessage(chat_id, message)

    else:       # Not found city
        errorCode = response.get('message')
        sendTextMessage(chat_id, str(resultCode) + ' - ' + errorCode)



"""
    Location input request
    Makes request to Openweathermap to fetch weathercast
"""
def locationInputRequest(latitude, longitude):
    if not latitude or not longitude:
        logging.warning('Error: - responseController.locationInputRequest: No lat or lng input')

    try:
        urlEncodePairs = { 'lat': str(latitude), 'lon': str(longitude), 'APPID': WEATHER_API_KEY, 'units': WEATHER_UNIT, 'cnt': WEATHER_DAY_CNT }
        encodedURL = urllib.urlencode(urlEncodePairs)

        WEATHER_URL_COORD = WEATHER_BASE_URL + encodedURL

        weatherResponse = json.load(urllib2.urlopen(WEATHER_URL_COORD))

        return weatherResponse

    except Exception, e:
        logging.warning('Error: - responseController.locationInputRequest: ' + str(e))





"""
    Text response handler
    Parses Openweathermap @response and sends the information to user at specified @chat_id
"""
def textInputHandler(chat_id, response):
    resultCode = response['cod']

    if resultCode == 200:       # Success city found
        cityName = response.get('name')
        countryName = response.get('sys').get('country')
        temp_current = response.get('main').get('temp')
        temp_max = response.get('main').get('temp_max')
        temp_min = response.get('main').get('temp_min')
        description = response.get('weather')[0].get('description')
        description_brief = response.get('weather')[0].get('main')
        
        weatherID = response.get('weather')[0].get('id')     # gets ID of weather description, used for emoji
        emoji = getEmoji(weatherID)
        
        message = cityName + ', ' + countryName + ': ' + str(temp_current) + degree_sign + 'C\n' + 'Max: ' + str(temp_max) + degree_sign + 'C - ' + 'Min: ' + str(temp_min)+ degree_sign  + 'C\n' + description_brief + ' - ' + description + emoji + emoji
            
        sendTextMessage(chat_id, message)
        
    else:       # Not found city
        errorCode = response.get('message')
        sendTextMessage(chat_id, str(resultCode) + ' - ' + errorCode)



"""
    Text input request
    Makes request to Openweathermap to fetch weathercast
"""
def textInputRequest(text):
    if not text:
        logging.warning('Error: - responseController.textInputRequest: No text input')

    try:
        urlEncodePairs = { 'q': text, 'APPID': WEATHER_API_KEY, 'units': WEATHER_UNIT, 'cnt': WEATHER_DAY_CNT }
        encodedURL = urllib.urlencode(urlEncodePairs)

        WEATHER_URL_TEXT = WEATHER_BASE_URL + encodedURL

        weatherResponse = json.load(urllib2.urlopen(WEATHER_URL_TEXT))

        return weatherResponse

    except Exception as e:
        logging.warning('Error: - responseController.textInputRequest: ' + str(e))



"""
    Send text message to user
"""
def sendTextMessage(chat_id, text=None):
    if(not chat_id or not text):
        logging.warning('chat_id or text is not entered')

    try:
        message = urllib.urlencode({ 'chat_id': format(chat_id), 'text': text.encode('utf-8', 'strict'), 'disable_web_page_preview': True })
        response = urllib.urlopen(BASE_URL + 'sendMessage', message.encode('utf-8'))

        logging.info('send response:')
        logging.info(response.read())
    except Exception as e:
        logging.warning('Error - responseController.sendTextMessage: ' + str(e))
        return



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
            return defaultEmoji    # Default emoji

    else:
        return defaultEmoji   # Default emoji