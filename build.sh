#!/bin/bash

set -e

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

# 2. Build Redocly docs

echo "Updating API reference docs..."
redocly build-docs schema.yml --output=docs/index.html

# 3. Update Python SDK
echo "Regenerating SDK..."
speakeasy run
echo "SDK successfully updated."

