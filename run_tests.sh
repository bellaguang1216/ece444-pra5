#!/bin/bash

# Quick test runner script
# Usage: ./run_tests.sh [eb-url]

if [ -z "$1" ]; then
    echo "Usage: ./run_tests.sh <eb-url>"
    echo "Example: ./run_tests.sh http://my-app.elasticbeanstalk.com"
    exit 1
fi

export API_URL="$1"
echo "Testing API at: $API_URL"
echo ""

python test_api.py

