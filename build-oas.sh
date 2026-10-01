#!/bin/bash

set -e

echo "Generating OAS file..."
python manage.py spectacular --color --file schema.yml
sleep .5

# Verify schema was generated successfully
if [ $? -ne 0 ]; then
    echo "Failed to generate schema" 
    exit 1
else
    echo "Schema generated!"
fi
