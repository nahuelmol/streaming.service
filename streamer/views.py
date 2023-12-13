from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from json.decoder import JSONDecodeError

import subprocess
import json
import psutil
import time

@csrf_exempt
def sendRTMP(req):

	#command = 'ffmpeg -i D:\\djangopros\\stream_site\\samples\\taladro.mp4 -c:v libx264 -preset veryfast -c:a aac -f flv rtmp://localhost:1935/live/stream' 
	command = ['ffmpeg', '-i', 'D:\\djangopros\\stream_site\\samples\\taladro.mp4', '-c:v', 'libx264', '-preset', 'veryfast', '-c:a', 'aac', '-f', 'flv', 'rtmp://localhost:1935/live/stream']

	if req.method == 'GET':

		try:
			process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			msg = 'ffmpeg runnig asynchronously'
			return HttpResponse(msg)

		except Exception as e:
			print(e)
			return HttpResponse(f"Error: {e}")

	if req.method == 'POST':

		try:

			if isinstance(req.body, bytes):

				json_str = req.body.decode('utf-8')
				json_obj = json.loads(json_str)

				name = json_obj["name"]
				lastname = json_obj["lastname"]
				phrase = json_obj['command']

				pabs 	= phrase.split()[:1]
				cmd 	= pabs[0]

				if cmd == 'play':
					pabs 	= phrase.split()[:2]
					filename = pabs[1]
					filecmd = 'ffmpeg -i D:\\djangopros\\stream_site\\samples\\' + filename + '.mp4'
					conf = '-c:v libx264 -preset veryfast -c:a aac -f flv http://localhost:1935/live/stream'

					complete_cmd = filecmd + ' '+ conf

					subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


			msg = 'POST request received ' + name + " "+ lastname 

			return HttpResponse(msg)

		except JSONDecodeError as json_error:
			error_msg = f"JSON decode error: {json_error}"
			return HttpResponse(error_msg, status=400)

		except Exception as e:
			error_msg = f"Error processing POST request: {e}"
			return HttpResponse(error_msg, status=500)

	if req.method == 'HEAD':
		try:
			process_running = any(
                process.name() == 'ffmpeg' and 'http://localhost:1935/live/stream' in process.cmdline()
                for process in psutil.process_iter(['pid', 'name', 'cmdline'])
                )
				
			if process_running:
				msg = 'ffmpeg process is running'
			else:
				msg = 'ffmpeg process is not running'
			
			return HttpResponse(msg)

		except Exception as e:
			print(e)
			return HttpResponse(f"Error: {e}")

	return HttpResponse("Invalid HTTP method")