import os
import pandas as pd
import json
import requests
from flask import Flask, request, Response

# Constant
token = '6216712870:AAFdNG5QZXsUFUog1PAfXKj23dcyXxQaw1s'

# https://api.telegram.org/bot6216712870:AAFdNG5QZXsUFUog1PAfXKj23dcyXxQaw1s/setWebhook?url=https://c902c6fcf97f39.lhr.life

def send_message(chat_id,text):
	url = 'https://api.telegram.org/bot{}'.format(token)
	url = url + '/sendMessage?chat_id={}'.format(chat_id)

	r = requests.post(url,json={'text': text})

	print('Status Code {}'.format(r.status_code))

	return None

def predict(data):

	# API CALL
	# Local API
	# url = 'http://127.0.0.1:5000/genres_pred/predict'
	
	# API in Production
	url = 'https://jbm-genrepred-deploy-og1d.onrender.com/genres_pred/predict'
	
	header = {'Content-type': 'text/plain'}
	data = data

	r = requests.post(url,data=data,headers=header)

	print('Status Code {}'.format(r.status_code))

	r_json = r.json()
	genres = r_json[0]
	genre_str = ", ".join(genres)

	return genre_str


def parse_message(message):

	chat_id = message['message']['chat']['id']
	sinopse = message['message']['text']

	sinopse = sinopse.replace('/','')

	try:
		sinopse = str(sinopse)

	except ValueError:
		sinopse = 'error'

	return chat_id, sinopse


# API Initialize
app = Flask(__name__)

@app.route('/',methods=['GET','POST'])

def index():
	if request.method == 'POST':
		message = request.get_json()

		chat_id, sinopse = parse_message(message)

		if sinopse != 'error':
			# Loading data
			data = sinopse

			d1 = predict(data)

			# Define Message to return
			msg = 'Genres Predicted: {}'.format(d1)

			# Send Message
			send_message(chat_id,msg)
			return Response('OK',status=200)

		else:

			send_message(chat_id,'The synopsis must be a string')
			return Response('OK',status=200)
	else:
		return '<h1> Genres Movies Prediction Telegram Bot </h1>'

if __name__ == '__main__':
	port = os.environ.get('PORT',5000)
	app.run(host='0.0.0.0',port=5000)
