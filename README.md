# EmbeddedCD
A temperature and humidity recording system in the Raspberry Pi.

The files in static are about html and related library.

The function of weather.py:
1. Create the data base.  "python3 weather.py create"
2. Get data from the sensor and write to the DB every ten seconds.  "python3 weather.py"
3. Show all the data. "python3 weather.py show"

The function of bked.py:

Open the flask serve, get the data and send it to the related api.

The function of pyQTchart.py:

Show the real-time temperature and humidity by using QT.

The picture of html:
![image](https://github.com/blacktion/EmbeddedCD/blob/master/effect-pictures/html.png?raw=true)

The picture of pyQT:
![image](https://github.com/blacktion/EmbeddedCD/blob/master/effect-pictures/pyqtchart.png?raw=true)
