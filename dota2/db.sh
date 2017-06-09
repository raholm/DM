#!/bin/bash

function start_mongodb {
	mongod --dbpath $D2_DB_PATH --auth
}

function login_mongodb {
	mongo -u $D2_DB_USERNAME -p $D2_DB_PASSWORD $D2_DB_NAME
}

command="$1"

if [ "$command" == "start" ]; then
	start_mongodb
elif [ "$command" == "login" ]; then
	login_mongodb
else
	echo "unknown"
fi

