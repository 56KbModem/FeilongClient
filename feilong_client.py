#!/usr/bin/env python3

# External library includes
import requests
import json

welcome_message = """
>>>> [!] Feilong REST API Client [!] <<<<
please configure the payload file according to
what URL you want to send. If you choose to
send a POST request then please note that you
Have to fill out a JSON object file that corresponds
with the request you are willing to make.
"""
def print_menu():
	print("""
[+] MENU
1: send GET request
2: send POST request
3: print menu text again
4: exit program
""")

def exit_program():
	print("Goodbye!")
	exit(0)


# Send a HTTP GET request to the
# Feilong API...
def send_get_request():
	api_name = input("Please provide the API name: ")
	request_url = '{0}:{1}/{2}'.format(feilong_server, feilong_port, api_name)
	response = requests.get(request_url)

	print(response.text)

# Send a HTTP POST request to
# the Feilong API...
def send_post_request():
	api_name = input("Please provide the API name: ")
	request_url = '{0}:{1}/{2}'.format(feilong_server, feilong_port, api_name)

	# Read the data for POST request
	json_file = open("data.json", 'r')
	json_data = json.read(json_file)
	json_file.close()

	response = requests.post(request_url)

	print

# Use a dispatch table technique to
# choose which function we will execute
def switch_choice(user_choice):
	table = {
		1: send_get_request,
		2: send_post_request,
		3: print_menu,
		4: exit_program
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
			switch_choice(user_choice)
		except ValueError as e:
			print("[ERROR]: Please use a valid integer for a choice!")
			print("[DEBUG]: error: {0}".format(e))
			user_value = 0 # clear user value!
