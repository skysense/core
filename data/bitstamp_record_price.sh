#!/usr/bin/env bash
while true; do wget https://www.bitstamp.net/api/ticker -O out/$(date -d "today" +"%Y%m%d-%H%M%S").json; sleep 5; done;