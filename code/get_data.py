from get_api import get_api
import datetime

#Url: https://api.open-meteo.com/v1/forecast?latitude=21.0245&longitude=105.8412&hourly=temperature_2m&timezone=Asia%2FSingapore

hanoi_geographic_coordinates = {
    "lat": 21.0245,
    "lon": 105.8412,
    "timezone": r"Asia%2FSingapore"
}

data = get_api(hanoi_geographic_coordinates["lat"], hanoi_geographic_coordinates["lon"], hanoi_geographic_coordinates["timezone"])
dateandtime = data["hourly"]["time"]
temperature = data["hourly"]["temperature_2m"]
records = 0
for i in dateandtime:
    records += 1

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

main_file = BASE_DIR / "csv" / "weather.csv"
draft_file = BASE_DIR / "csv" / "nomatch.csv"



# Write header only if main file is empty
with open(main_file, 'a+') as f:
    f.seek(0)
    if f.read() == "":
        f.write("datetime,temperature,write at\n")
        print(f"Wrote title to file <{main_file}> successfully")

# Overwrite draft file with the new records
write_time = datetime.datetime.now()
with open(draft_file, 'w') as k:
    for i in range(records):
        k.write(f"{dateandtime[i]},{temperature[i]},{write_time}\n")
print(f"Wrote {records} lines to draft file <{draft_file}> successfully")

# Compare draft against main file, line by line (skipping the header)
def key_fields(line):
    parts = line.strip().split(",")
    return (parts[0].strip(), parts[1].strip())

# Read existing main file (keys only) and the draft rows
with open(main_file, 'r') as f:
    main_lines = f.readlines()

with open(draft_file, 'r') as k:
    draft_lines = k.readlines()

# Build a set of keys already in main (skip header)
existing_keys = {key_fields(line) for line in main_lines[1:] if line.strip()}

# Keep only draft rows whose datetime/temperature aren't in main yet
new_rows = [line for line in draft_lines
            if line.strip() and key_fields(line) not in existing_keys]

# Append the new rows to the main file
if new_rows:
    with open(main_file, 'a') as f:
        f.writelines(new_rows if new_rows[-1].endswith("\n") else
                     [r if r.endswith("\n") else r + "\n" for r in new_rows])
    print(f"Appended {len(new_rows)} new rows to <{main_file}>")
else:
    print("No new rows to append")

# Truncate the draft file
with open(draft_file, 'w') as k:
    pass
print(f"Truncated draft file <{draft_file}>")