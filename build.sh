#!/bin/bash

set -e

PATH_TO_SCHEMA="$HOME/Code/portfolio-projects/fstop-docs/"

# 1. Update OAS file

echo "Generating OAS file..."
python3 manage.py spectacular --color --file schema.yml
sleep .5

# Verify schema was generated successfully
if [ $? -ne 0 ]; then
    echo "Failed to generate schema" 
    exit 1
else
    echo "Schema generated!"
fi