#!/usr/bin/env python3

# Simple Feilong API Client
# November 2019
# Nick Snel - ICU IT Services

# External library includes
import requests # for accessing the REST API
import json # for manipulating JSON data
from time import strftime, localtime # for timestamping
import os, subprocess # for calling our editor, checking environ


# Global configuration
config_file = open("config.json", 'r') # config file
config = json.load(config_file)
feilong_server = config["config"]["server_ip"] # global ip address
feilong_port = config["config"]["server_port"] # global tcp-port 
config_file.close()

# Set file editor
EDITOR = os.environ.get('EDITOR') if os.environ.get('EDITOR') else 'vim'

welcome_message = """>>>> [!] Feilong REST API Client [!] <<<<

"""

# This function is used to edit the
# configuration, then writes it
# back into the file.
def configure():
	global feilong_server, feilong_port
	config_file = open("config.json", 'w')
	feilong_server = input("New server IP address: ")
	feilong_port = input("New server TCP port: ")

	# configure with new parameters
	config["config"]["server_ip"] = feilong_server
	config["config"]["server_port"] = feilong_port

	json_object = json.dumps(config, sort_keys=True, indent=4)
	config_file.write(json_object)
	config_file.close()

def print_menu():
	print("""
[!] CONFIG
[!] SERVER IP: {0}
[!] SERVER PORT: {1}

[+] MENU
1: send GET request
2: send POST request
3: send DELETE request
4: configure client
5: print this menu again
6: exit program
""".format(feilong_server, feilong_port))

def exit_program():
	print("Goodbye!")
	exit(0)


# Send a HTTP GET request to the
# Feilong API...
def send_get_request():
	api_name = input("Please provide the API name: ")
	request_url = 'http://{0}:{1}/{2}'.format(feilong_server, feilong_port, api_name)
	response = requests.get(request_url)

	# Log the event
	event = {"last_query": request_url}
	event["last_query_time"] = strftime("%Y-%m-%d %H:%M:%S", localtime())
	log_event(event)

	print("[+] RESPONSE: \n{0}".format(response.text))

# Send a HTTP POST request to
# the Feilong API...
def send_post_request():
	api_name = input("Please provide the API name: ")
	request_url = 'http://{0}:{1}/{2}'.format(feilong_server, feilong_port, api_name)
	
	# Read the data for POST request
	# Open a file with the same api name
	# ending with the suffix '.json'
	json_file = open("request_data/" + api_name + ".json", 'r')
	json_data = json.load(json_file)
	json_file.close()

	editing = 1   # do we want to edit the request? default to yes when ran first time
	while editing:
		print("[!] Preview of request:\n{0}".format(json_data))
		user_input = input("[S]end request, [E]dit file (make sure to save!), [A]bort: ")
		if user_input.upper() == 'S':
			editing = 0
			print("[+] sending post request to {0}:{1}".format(feilong_server, feilong_port))

			# send the POST request
			headers = {'content-type': 'application/json'}
			response = requests.post(request_url, data=json.dumps(json_data), headers=headers)

			# Log the event
			event = {"last_query": request_url}
			event["last_query_time"] = strftime("%Y-%m-%d %H:%M:%S", localtime())
			log_event(event)

			print("[+] RESPONSE: \n{0}".format(response.text))

		# Edit the data, save it to the file and reload it
		elif user_input.upper() == 'E':
			subprocess.call([EDITOR, "request_data/" + api_name + ".json"])
			json_file = open("request_data/" + api_name + ".json", 'r')
			json_data = json.load(json_file)
			json_file.close()			

		elif user_input.upper() == "A":
			editing = 0
			print("[+] Aborting...")
		else:
			user_input = input("[S]end request, [E]dit file, [A]bort: ")

def send_delete_request():
	user_id = input("Please provide the userid to delete: ")
	request_url = "http://{0}:{1}/guests/{2}".format(feilong_server, feilong_port, user_id)

	print("Sending delete API call for user: {0}".format(user_id))
	response = requests.delete(request_url)
	print("[+] RESPONSE:\n{0}".format(response.text))

# Log requests back into our config file
# uses local system clock in event
# param: event: dictionary holding
# last query made and the timestamp
def log_event(event=None):
	if event == None:
		return
	else:
		config_file = open("config.json", 'r')
		config = json.load(config_file)
		config_file.close()

		# Update new event
		config["diagnostics"].update(event)
		config["diagnostics"]["request_count"] += 1	

		# Write back to config file
		config_file = open("config.json", 'w')
		config_file.write(json.dumps(config, sort_keys=True, indent=4))
		config_file.close()


# Main function
if __name__ == "__main__":

	# Use a dispatch table technique to
	# choose which function we will execute	
	table = {
		1: send_get_request,
		2: send_post_request,
		3: send_delete_request,
		4: configure,
		5: print_menu,
		6: exit_program
	}

	print(welcome_message)
	print_menu()

	while True:
		try:
			user_choice = int(input("[menu] > "))
			if user_choice in range(1, len(table)+1):
				func = table.get(user_choice, lambda: "Invalid choice")
				func()
		except ValueError as e:
			print("[ERROR]: Please use a valid integer for a choice!")
			print("[DEBUG]: error: {0}".format(e))
			user_choice = 0 # clear user value!
