import json
import os

# Check if clone_before.json exists, otherwise create an empty structure
if os.path.exists('clone_before.json'):
    with open('clone_before.json', 'r') as fh:
        before = json.load(fh)
else:
    before = {"clones": [], "count": 0, "uniques": 0}

# Read current clone.json data
with open('clone.json', 'r') as fh:
    now = json.load(fh)

# Build a dictionary of timestamps from the previous data
timestamps = {before['clones'][i]['timestamp']: i for i in range(len(before['clones']))}

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

# Compress old data to reduce size
if len(timestamps) > 100:
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

# Save the updated clone data to clone.json
with open('clone.json', 'w', encoding='utf-8') as fh:
    json.dump(latest, fh, ensure_ascii=False, indent=4)

