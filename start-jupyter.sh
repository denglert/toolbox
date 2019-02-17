#!/usr/bin/env bash

#source setup.sh
if  [ -z "${TOOLBOX_DIR}" ]; then
	echo "TOOLBOX_DIR variable not set up. Sourcing toolbox/setup.sh script..."
	BASEDIR=$(dirname $(realpath "$BASH_SOURCE"))
	source ${BASEDIR}/setup.sh
fi


PORT=$1
BROWSER=$2

if  [ -z "${PORT}" ]; then
	PORT=8888
	echo "PORT=${PORT}"
fi


if  [ -z "${BROWSER}" ]; then
	echo "No browser selected."
	jupyter notebook --no-browser --port=${PORT}

else
	echo "BROWSER=${BROWSER}"
	jupyter notebook --browser=${BROWSER} --port=${PORT}
fi


