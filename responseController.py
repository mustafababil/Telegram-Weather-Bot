
import urllib

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

################################################

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