#!/usr/bin/env python3

# External library includes
import requests
import json

# Global configuration
config_file = open("config.json", 'r')
config = json.load(config_file)
feilong_server = config["config"]["server_ip"]
feilong_port = config["config"]["server_port"]

welcome_message = """>>>> [!] Feilong REST API Client [!] <<<<
please configure the payload file according to
what URL you want to send. If you choose to
send a POST request then please note that you
Have to fill out a JSON object file that corresponds
with the request you are willing to make.
"""

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
3: configure client
4: print this menu again
5: exit program
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

	print(response.text)

# Send a HTTP POST request to
# the Feilong API...
def send_post_request():
	editing = 1   # do we want to edit the request?
	api_name = input("Please provide the API name: ")
	request_url = 'http://{0}:{1}/{2}'.format(feilong_server, feilong_port, api_name)
	

	# Read the data for POST request
	# Open a file with the same api name
	# ending with the suffix '.json'
	json_file = open("request_data/" + api_name + ".json", 'r')
	json_data = json.load(json_file)
	json_file.close()

	while editing:
		print("[!] Preview of request:\n{0}".format(json_data))
		user_input = input("Do you wish to edit some of the parameters? [Y/n]: ")
		if user_input == 'Y' or user_input == 'y':
			key = input("Key to edit: ")
			value = input("New value for key: ")

			try:
				json_data[key] = value
			except KeyError:
				print("The key {key} does not exist".format(key))

		elif user_input == 'N' or user_input == 'n':
			editing = 0
			print("[+] Sending POST request!")
			
		else:
			print("Please use")

# Use a dispatch table technique to
# choose which function we will execute
def switch_choice(user_choice):
	table = {
		1: send_get_request,
		2: send_post_request,
		3: configure,
		4: print_menu,
		5: exit_program
	}

	# execute desired function
	func = table.get(user_choice, lambda: "Invalid choice")
	func()

if __name__ == "__main__":
	print(welcome_message)
	print_menu()

	while True:
		try:
			user_choice = int(input("[menu] > "))
		except ValueError as e:
			print("[ERROR]: Please use a valid integer for a choice!")
			print("[DEBUG]: error: {0}".format(e))
			user_value = 0 # clear user value!
			
		switch_choice(user_choice)
