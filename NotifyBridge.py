#!/usr/bin/env python3

## author: @oranja [ oranja at gmail dot com ]
#
## A simple HTTP-activated notification server
#
## Based on the work of @primalcortex
## https://primalcortex.wordpress.com/2014/09/23/monit-and-kde-desktop-notifications/

import gi
gi.require_version('Notify', '0.7')

from gi.repository import Notify
from flask import Flask, request
from flask_json import FlaskJSON, JsonError, json_response, as_json

app = Flask(__name__)
FlaskJSON(app)
	
## Constants definition
APP_NAME = 'NotifyBridge'
DEBUG = False
HOST = '0.0.0.0'    # Host IP Address. '' allows only localhost access. '0.0.0.0' allows connections on any interface.
PORT = 29876    # Listening port. Choose any above 1024. The client must use the same port...
ADDR = (HOST, PORT)


def log(message):
	print('{}: {}'.format(APP_NAME, message))

## Send notification for the KDE notification system
def notify(title, body, icon=None):
	notification = Notify.Notification.new(title, body, icon)
	notification.show()


@app.route('/notify/jenkins/build/start', methods=['POST'])
def handle_notify_jenkins_build_start():
	data = request.get_json(force=True)
	job_name = data['name']
	build_name = '#{}'.format(data['build']['number'])
	build_url = data['build']['full_url']
	
	title = 'Jenkins: Build Started'
	body = '{} [<a href="{}">{}</a>]'.format(job_name, build_url, build_name)
	icon = 'applications-development'
	notify(title, body, icon)
	return json_response()
	
@app.route('/notify/jenkins/build/result', methods=['POST'])
def handle_notify_jenkins_build_end():
	data = request.get_json(force=True)
	job_name = data['name']
	build_name = '#{}'.format(data['build']['number'])
	build_url = data['build']['full_url']
	build_status = data['build']['status']
	
	title = 'Jenkins: Build Result'
	body = '{} [<a href="{}">{}</a>] :: {}'.format(job_name, build_url, build_name, build_status)
	icon = 'flag-red'
	if build_status == 'SUCCESS':
		icon = 'flag-green'
	notify(title, body, icon)
	return json_response()


if __name__ == '__main__':
	log('Initializing the server...')
	Notify.init(APP_NAME)
	app.run(debug=DEBUG, port=PORT)
	log("Shutting down...")
	Notify.uninit()
	log("Bye")
