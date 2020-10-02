#!/bin/bash

if [ -z "$WAITFOR" ] ; then
  echo "No service dependencies"
else
  echo "Waiting for service dependencies..."
  for service in ${WAITFOR//,/ }
  do
    addr=(${service//:/ })
    echo "Waiting for ${addr[0]} to start service on port ${addr[1]}"
    while ! nc -z ${addr[0]} ${addr[1]}; do
      sleep 0.1
    done
    echo "${addr[0]} started service on port ${addr[1]}"
  done
  echo "All dependencies started!"
fi

echo "Ready to start"
echo $@
exec $@
