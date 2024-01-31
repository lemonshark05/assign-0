#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: ./run-stats.sh <lir_file> <json_file>"
    exit 1
fi

LIR_FILE="$1"
JSON_FILE="$2"

if [ -f "$LIR_FILE" ]; then
    python lir_parse.py "$LIR_FILE"
elif [ -f "$JSON_FILE" ]; then
    # python read_json.py "$JSON_FILE"
else
    echo "Error: Neither LIR nor JSON file exists."
    exit 1
fi
