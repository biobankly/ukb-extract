import json
import os

def debug_log(message):
    """Print debug messages for GitHub Actions log."""
    print(f"::debug::{message}")

# Load current clone data from the GitHub API
if os.path.exists("current_clones.json"):
    debug_log("Loading current_clones.json fetched from GitHub API.")
    with open("current_clones.json", "r") as fh:
        now = json.load(fh)
else:
    debug_log("current_clones.json not found. Exiting script.")
    raise FileNotFoundError("current_clones.json not found. Ensure it exists before running the script.")

# Load previous clone data from clone.json
if os.path.exists("clone.json"):
    debug_log("Loading clone.json.")
    with open("clone.json", "r") as fh:
        before = json.load(fh)
else:
    debug_log("clone.json not found. Exiting script.")
    raise FileNotFoundError("clone.json not found. Ensure it exists in the repository.")

# Build a dictionary of timestamps from the previous data
timestamps = {before['clones'][i]['timestamp']: i for i in range(len(before['clones']))}
debug_log(f"Existing timestamps: {timestamps}")

# Merge current clone data with previous data
latest = dict(before)
for i in range(len(now['clones'])):
    timestamp = now['clones'][i]['timestamp']
    if timestamp in timestamps:
        latest['clones'][timestamps[timestamp]] = now['clones'][i]
    else:
        latest['clones'].append(now['clones'][i])

# Update count and uniques
latest['count'] = sum(map(lambda x: int(x['count']), latest['clones']))
latest['uniques'] = sum(map(lambda x: int(x['uniques']), latest['clones']))
debug_log(f"Updated counts: Total - {latest['count']}, Uniques - {latest['uniques']}")

# Save updated data to clone.json
debug_log("Saving updated clone data to clone.json.")
with open("clone.json", "w", encoding="utf-8") as fh:
    json.dump(latest, fh, ensure_ascii=False, indent=4)
