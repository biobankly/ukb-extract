import json
import os

def debug_log(message):
    """Print debug messages for GitHub Actions log."""
    print(f"::debug::{message}")

# Check for clone_before.json or initialize
if os.path.exists('clone_before.json'):
    debug_log("Loading clone_before.json.")
    with open('clone_before.json', 'r') as fh:
        before = json.load(fh)
else:
    debug_log("clone_before.json not found. Initializing new data structure.")
    before = {"clones": [], "count": 0, "uniques": 0}

# Check for clone.json or exit with error
if os.path.exists('clone.json'):
    debug_log("Loading clone.json.")
    with open('clone.json', 'r') as fh:
        try:
            now = json.load(fh)
        except json.JSONDecodeError:
            debug_log("Error decoding clone.json. Initializing as empty.")
            now = {"clones": []}
else:
    debug_log("clone.json not found. Exiting script.")
    raise FileNotFoundError("clone.json not found. Ensure it exists before running the script.")

# Validate structure of now
if "clones" not in now:
    debug_log("No 'clones' key found in clone.json. Initializing as empty list.")
    now["clones"] = []

# Merge data
timestamps = {before['clones'][i]['timestamp']: i for i in range(len(before['clones']))}
debug_log(f"Existing timestamps: {timestamps}")

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

# Compress old data
if len(timestamps) > 100:
    debug_log("Compressing old data to reduce size.")
    remove_this = []
    clones = latest['clones']
    for i in range(len(timestamps) - 35):
        clones[i]['timestamp'] = clones[i]['timestamp'][:7]
        if clones[i]['timestamp'] == clones[i + 1]['timestamp'][:7]:
            clones[i + 1]['count'] += clones[i]['count']
            clones[i + 1]['uniques'] += clones[i]['uniques']
            remove_this.append(clones[i])

    for item in remove_this:
        clones.remove(item)

# Save updated data to clone.json
debug_log("Saving updated clone data to clone.json.")
with open('clone.json', 'w', encoding='utf-8') as fh:
    json.dump(latest, fh, ensure_ascii=False, indent=4)
