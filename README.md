Telegram Weather Bot
===================


[@weathercast_bot](http://telegram.me/weathercast_bot)
----------


This [Telegram Bot](https://core.telegram.org/bots/api) takes user's location as **text** or **GPS coordinates** and then informs about its current weather-cast. 

Weather information is supplied by *OpenWeatherMap*.

Bot sends current temperature as well as minimum and maximum expectations.
It adds description of the weather with reflecting emoji. :sunny: :umbrella: :snowman: 

This project is prepared to be deployed **Google App Engine** and works with Webhooks.

----------

Details
-------------

main.py						=> Fethces the user input and calls the related functions
inputModel.py				=> To parse the user input which is JSON format
responseController.py => For *text* and *GPS coordinates* inputs, it makes the Openweathermap API calls and prepares response messages to the users

[Installing at Google App Engine instructions](https://github.com/yukuku/telebot/blob/master/README.md)


Thanks [yukuku](https://github.com/yukuku) for the basic project.

---------
   
TODO
-------------------

 1. Fit Openweathermap API response to a model
 2. Create Database for Daily/Hourly Notifications and related settings

---------

Screenshots
-------------

**Bot start screen**

----------
![telegram @weathercast_bot start screen](http://i.imgur.com/wBLWQXL.png "telegram weathercast bot start")

----------

**Input location as text or GPS coordinates**

----------
![bot text or gps input](http://i.imgur.com/6ECnXbX.png "bot text or gps input")

----------

**Bot options**

----------
![bot options](http://i.imgur.com/RoPRjip.jpg "bot options")

----------

**Error when city not found**

----------
![404-city not found](http://i.imgur.com/lc03aYs.jpg "404-city not found")

