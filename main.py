import json
import os

def debug_log(message):
    """Print debug messages for GitHub Actions log."""
    print(f"::debug::{message}")

# Load clone.json, which contains the API response
try:
    with open("clone.json", "r") as fh:
        now = json.load(fh)
except (FileNotFoundError, json.JSONDecodeError):
    debug_log("Failed to load or decode clone.json. Initializing new data structure.")
    now = {"clones": [], "count": 0, "uniques": 0}

# Validate structure of clone.json
if "clones" not in now:
    debug_log("No 'clones' key found in clone.json. Initializing as empty list.")
    now["clones"] = []

# Aggregate clone data
timestamps = {entry["timestamp"]: entry for entry in now["clones"]}
debug_log(f"Current timestamps: {timestamps}")

# Merge and update counts
total_clones = sum(entry["count"] for entry in now["clones"])
unique_clones = sum(entry["uniques"] for entry in now["clones"])
now["count"] = total_clones
now["uniques"] = unique_clones

debug_log(f"Updated counts: Total - {now['count']}, Uniques - {now['uniques']}")

# Save the updated clone.json
with open("clone.json", "w", encoding="utf-8") as fh:
    json.dump(now, fh, ensure_ascii=False, indent=4)
debug_log("Saved updated clone.json.")
