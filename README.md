# Raspberry Pi Temperature Logger

This repo contains code for a Raspberry Pi temperature logger which uses SQLite to store data read from a DS18B20 sensor.  

There are several scripts that can be used. You'll need to trigger regular temperature logging from a cron job

## Scripts

`check_results.py` - Use to check the DB contents

`logger.py` - Used to log the temps into the DB, driven from a cron job

`webgui.py` - Drives a webpage to visualise the results

## Original info

This was all created originally from this website (which seems to be offline currently):

http://raspberrywebserver.com/cgiscripting/rpi-temperature-logger/building-an-sqlite-temperature-logger.html


