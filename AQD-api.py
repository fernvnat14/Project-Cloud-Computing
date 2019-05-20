from flask_cors import CORS
from flask import Flask, request
from flask_restful import Resource, Api
import json
import random
import requests

#url1 = 'http://35.231.245.160:5000/notify/user/AQD Status:'
#response1 =0
#response2 =0
#response3 =0
#token = 'rr9Zm0rpWgf0wb6iHEVY5EigwgTI99iFlOarNzeAutq'
#headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}

#msg = 'hello'
#r = requests.post(url, headers=headers , data = {'message':msg})
#print r.text

app = Flask(__name__)
CORS(app)
api = Api(app)


import time

def check_air_status(x):
        if x <= 50:
                return 'Good'
        elif 51 <= x <= 100:
                return 'Moderate'
        elif 101 <= x <= 150:
                return 'Unhealthy for Sensitive Groups'
        elif 151 <= x <= 200:
		#response1 = requests.get(url1+'Unhealthy/none')
                return 'Unhealthy'
        elif 201 <= x <= 300:
		#response2 = requests.get(url1+'Very Unhealthy/none')
                return 'Very Unhealthy'
        elif x > 300:
		#response3 = requests.get(url1+'Hazadous/none')
                return 'Hazadous'

@app.route('/api/v1/AQD/sensor_id/<id>')
def air_quality(id=None):
	url = "https://cie-smart-city.appspot.com/sensors/sensor_id/" + id
	response = requests.get(str(url))
	air_status = response.json()
	print(air_status)
	data = {"id":air_status["id"], "data":{"status":check_air_status(int(air_status["data"]))}, "location":{"coordinate":air_status["location"]["coordinate"]}}
	return json.dumps(data)

@app.route('/api/v1/AQD', methods=['GET', 'POST'])
def get_allbinstatus():
        url = "https://cie-smart-city.appspot.com/sensors/project_id/AQD"
        response = requests.get(str(url))
        air_status = response.json()
        print(air_status)
        all_data = []
        for i in range(len(air_status)):
            data = {"id":air_status[i]["id"], "data":{"status":check_air_status(int(air_status[i]["data"]))}, "location":{"coordinate":air_status[i]["location"]["coordinate"]}}
            all_data.append(data)
        return json.dumps(all_data)

if __name__ == '__main__':
     app.run(host="0.0.0.0", port=8080,debug=True)
