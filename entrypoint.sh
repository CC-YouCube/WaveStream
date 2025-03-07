#!/bin/ash

if [[ -n ${TOR} ]] ; then
  tor -f /etc/tor/torrc --RunAsDaemon 1
fi

python -m wavestream
