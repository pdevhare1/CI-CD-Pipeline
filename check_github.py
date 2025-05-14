import requests
import json
import os
import sys

# Configuration
REPO_OWNER = 'psagar-dev'
REPO_NAME = 'ci-cd-pipeline-bash-python'
BRANCH = 'main'
LAST_COMMIT_FILE = '/var/www/ci-cd-pipeline-bash-python/last_commit.txt'
GITHUB_API_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/commits/{BRANCH}"

def get_latest_commit_sha():
    """
    Fetch the latest commit SHA from the GitHub repository.
    """
    try:
        response = requests.get(GITHUB_API_URL, timeout=10)
        response.raise_for_status()
        commit_data = response.json()
        return commit_data['sha']
    except requests.RequestException as e:
        print(f"❌ Error fetching latest commit: {e}")
        return None
    except KeyError:
        print("❌ Unexpected response format.")
        return None

def read_stored_commit_sha():
    """
    Read the stored commit SHA from the file, if it exists.
    """
    if os.path.isfile(LAST_COMMIT_FILE):
        try:
            with open(LAST_COMMIT_FILE, 'r') as file:
                return file.read().strip()
        except IOError as e:
            print(f"❌ Error reading stored commit file: {e}")
    return None

def write_commit_sha(sha):
    """
    Write the latest commit SHA to the file.
    """
    try:
        with open(LAST_COMMIT_FILE, 'w') as file:
            file.write(sha)
    except IOError as e:
        print(f"❌ Error writing commit SHA: {e}")

def main():
    """
    Main execution function to compare and update commit SHA.
    Exits with:
    - 0 if new changes are found
    - 1 if no changes or on error
    """
    latest_sha = get_latest_commit_sha()
    if not latest_sha:
        sys.exit(1)

    stored_sha = read_stored_commit_sha()

    if latest_sha != stored_sha:
        print("✅ New changes detected.")
        write_commit_sha(latest_sha)
        sys.exit(0)
    else:
        print("ℹ️ No new changes.")
        sys.exit(1)

if __name__ == "__main__":
    main()
