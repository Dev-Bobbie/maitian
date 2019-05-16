#!/usr/bin/env bash

curl http://$1:6800/cancel.json -d project=maitian -d job=$2