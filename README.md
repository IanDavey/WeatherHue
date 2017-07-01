# WeatherHue
Make your Hue lights reflect the outside temperature.

Currently only supports a three-bulb first-generation A19 (LCT001) setup (i.e., the starter kit).

Some setup is required; namely, filling in your Wunderground key, a Hue bridge key, and your bridge's IP.

To run:
```
python3.6 weather-lights.py [--debug] [-l YOUR_ZIP_CODE]
```

Obviously, this comes with no warranty or support.
