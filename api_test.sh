#!/usr/bin/env bash

# API test script
# October 2019
# Nick Snel - ICU IT Services

# This was a prototype I made to quickly
# test Feilong about a month before I
# decided to rewrite it in python.
# For all intents and purposes this file
# should be viewed as deprecated.

## GLOBAL CONFIGURATION 
SERVER='192.168.100.200' # API server address
PORT=8080 # API server port
PAYLOAD_FILE='new_payload.http'
## !GLOBAL CONFIGURATION 


read_payload () {
	if [[ -f "$1" ]]; then
		local MY_PAYLOAD=$(cat $PAYLOAD_FILE);
	else
		echo "[-]: $PAYLOAD_FILE: no such file found";
		return -1;
	fi

	echo "$MY_PAYLOAD"; # this echo returns it to the caller
}

test_connection(){
	ping -c 4 -W 1 $SERVER &> /dev/null; # note the bash'ism here: "&>"
	if [ $? -eq 0 ]; then
		echo 0;
	else
		echo -1;
	fi
}

# Because bash can only return text from
# a subroutine I had no other option then
# to write 2 nearly identical functions...
# I know it is ugly.....

send_get_request () {
	echo "testing server connectivity";
	if [ test_connection -eq 0 ]; then
		RESPONSE=$(curl -s $SERVER:$PORT/"$1");
		echo -n '[+]: response: '
		echo $RESPONSE;
	else
		echo "[-] unable to connect to server: $SERVER:$PORT";
		return -1;
	fi
}

send_post_request() {
	echo "testing server connectivity";
	if [ test_connection -eq 0 ]; then
		RESPONSE=$(curl -X);
		echo -n '[+]: response: '
		echo $RESPONSE;
	else
		echo "[-] unable to connect to server: $SERVER:$PORT";
	fi
}

## ENTRY POINT
echo '>>>> [!] REST API test script [!] <<<<';

#PAYLOAD=$(read_payload $PAYLOAD_FILE);
REQUEST=$(head -n1 $PAYLOAD_FILE); # check request type
HTTP_TYPE=$(echo $REQUEST | awk '{print $1}');
LOCATION=$(echo $REQUEST | awk '{print $2}');

#echo "[DEBUG]: payload = $PAYLOAD";

echo -n '[?]: send payload to the server? [Y/n]: ';
read user_input;
if [[ $user_input == "Y" || $user_input == "y" ]]; then
	if [[ $HTTP_TYPE == 'GET' ]]; then
		echo '[+]: detected HTTP GET request';
		echo "[+]: request: $REQUEST";
		send_get_request $LOCATION;
		exit 0;
	fi
	if [[ $HTTP_TYPE == 'POST' ]]; then
		echo '[+]: detected HTTP POST';
	fi
else
	echo "[-]: not sending payload, goodbye!"
	exit 0;
fi
