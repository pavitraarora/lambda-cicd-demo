#!/bin/bash
# Exit immediately if any command fails
set -e

echo "Validating lambda_package.zip contents..."
# Check if lambda_function.py is at the root of the zip
unzip -l build/code/lambda_package.zip | awk '{print $4}' | grep -qx 'lambda_function.py' || { 
    echo "❌ ERROR: lambda_function.py is NOT at root"
    exit 1
}
echo "lambda_function.py is at root"
