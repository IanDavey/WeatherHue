#!/usr/bin/env python3.6

import argparse, math, json, requests, time

WUNDERGROUND_KEY = '***wunderground-key-here***'
HUE_KEY = '***hue-key-here***'
HUE_IP = '***hue-ip-here***'

COLORS = {
    115: [0.5224, 0.2373],
    105: [0.4964, 0.3552],
    95: [0.6736, 0.3221],
    85: [0.5503, 0.4139],
    75: [0.4651, 0.4422],
    65: [0.3933, 0.4869],
    55: [0.3257, 0.3535],
    45: [0.3804, 0.3768],
    35: [0.3032, 0.309],
    25: [0.1906, 0.0867],
    15: [0.2649, 0.1287],
    5: [0.3057, 0.2626],
    -5: [0.3783, 0.4574],
    -15: [0.3783, 0.4574]
}

parser = argparse.ArgumentParser(description='Make your Hue lights reflect the outside temperature')
parser.add_argument('-d', '--debug', action='store_true', dest='debug', help='Enable debugging output')
parser.add_argument('-l', '--location', action='store', dest='location', default='22902', help='The zipcode to query')
args = parser.parse_args()

while True:
    response = requests.get(f'http://api.wunderground.com/api/{WUNDERGROUND_KEY}/conditions/q/{args.location}.json')

    if response.status_code < 400:
        temperature = int(round(float(json.loads(response.content)['current_observation']['feelslike_f'])))

        if temperature in COLORS:
            value = COLORS[temperature]
        else:
            upper = 10 * math.ceil((temperature - 5) / 10) + 5
            lower = 10 * math.floor((temperature + 5) / 10) - 5
            offset = temperature - lower
            upper = COLORS[upper]
            lower = COLORS[lower]
            x = (upper[0] - lower[0]) / 10
            y = (upper[1] - lower[1]) / 10
            value = [x*offset + lower[0], y*offset + lower[1]]

        if args.debug:
            print(f'Temperature {temperature}; setting color to {value}...')

        for i in range(3):
            requests.put(f'http://{HUE_IP}/api/{HUE_KEY}/lights/{i+1}/state', json.dumps({'xy': value}))

    elif args.debug:
        print(f'Received {response.status_code} {response.reason} from Wunderground')

    time.sleep(300)
