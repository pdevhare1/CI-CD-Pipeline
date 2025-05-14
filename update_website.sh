#!/bin/bash
REPO_URL="https://github.com/psagar-dev/ci-cd-pipeline-bash-python.git"
REPO_DIR="/var/www/ci-cd-pipeline-bash-python"
WEBSITE_DIR="/var/www/html"
BRANCH_NAME="main"
LAST_COMMIT="/var/www/ci-cd-pipeline-bash-python/last_commit.txt"

# Pull latest changes
if [ ! -d "$REPO_DIR" ]; then
    echo "Creating repo directory: $REPO_DIR"
    mkdir -p "$REPO_DIR"
fi

cd "$REPO_DIR" || { echo "❌ Failed to enter $REPO_DIR"; exit 1; }

git fetch origin
git reset --hard "origin/$BRANCH_NAME"

if [ ! -f "$LAST_COMMIT" ]; then
    sudo touch "$LAST_COMMIT"
    echo "📄 Created: $LAST_COMMIT"
fi

# Copy files to website directory
rsync -av --delete $REPO_DIR/ $WEBSITE_DIR/
# This copies the new files to where Nginx can find them

# Restart Nginx
sudo systemctl restart nginx

# This restarts Nginx to make sure it sees the new files
echo "Website updated successfully"