#!/bin/bash
PROJECT_PATH="/var/www/ci-cd-pipeline-bash-python"

# Run the Python script to check for GitHub changes
python3 "$PROJECT_PATH/check_github.py"

# If the Python script exits with 0 (changes detected), run the update script
if [ $? -eq 0 ]; then
    echo "✅ Changes detected. Updating website..."
    bash "$PROJECT_PATH/update_website.sh"
else
    echo "ℹ️ No changes detected. No update needed."
fi