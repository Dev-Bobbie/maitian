#!/usr/bin/env bash

curl http://192.168.33.11:6800/schedule.json -d project=maitian -d spider=zufang
curl http://127.0.0.1:6800/schedule.json -d project=maitian -d spider=zufang