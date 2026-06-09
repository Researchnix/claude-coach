# Exploration of parser and libraries
# Execute line by line in a repl






import fitdecode
from collections import Counter






# This is the fit file I am trying this program on
filepath = 'fit/2026-05-21_Ride_i150396202.fit'

# Loading all frames with fitdecode into a list
with fitdecode.FitReader(filepath) as fit:
    frames = list(fit)

# there are Out[8]: 39564 frames in this activity
len(frames)

# Exploring the different frame types there are and
# how often they appear.
frame_types = Counter(type(frame) for frame in frames)
for key, value in frame_types.items():
    print(f"{value}:\t\t{key}")

# singling out the header frame for further inspection
header = next(f for f in frames if isinstance(f, fitdecode.records.FitHeader))
dir(header)

# trying to understand the data in this instance
for x in dir(header):
    # this works because this is a list of names of methods, not the methods themelves.
    if not x.startswith('_'):
        print(x, ':', getattr(header, x))

# dir lists methods and fields, this is how to distinguish them
for name in dir(header):
    if not name.startswith('_'):
        val = getattr(header, name)
        if callable(val):
            print('method:', name)
        else:
            print('field: ', name, '=', val)



# pruning out some frames to only keep the ones of type FitDataMessage
data_frames = [frame for frame in frames if isinstance(frame, fitdecode.FitDataMessage)]
len(data_frames)


# Among the type FitDataMessage are different frame names
# these are the different types of FitDataMessage types
# they have different frame.name values
names = Counter(frame.name for frame in data_frames)
for key, value in names.items():
    print(f"{value}:\t\t{key}")


#######################################################################################
# one by one disection of the different names
#######################################################################################


file_id = next(f for f in data_frames if f.name == "file_id")
dir(file_id)



zones_target = next(f for f in data_frames if f.name == "zones_target")

for name in dir(zones_target):
    if not name.startswith('_'):
        val = getattr(zones_target, name)
        if callable(val):
            print('method:', name)
        else:
            print('field: ', name, '=', val)

# drilling deeper even to explore the def_mesg instance in zones_target
for x in dir(zones_target.def_mesg):
    print(x)

zones_target.get_raw_value('def_mesg')

for field in zones_target.fields:
    print(field.name, ':', field.value)


# there are 14 time_in_zone frames
time_in_zone_list = [f for f in data_frames if f.name == 'time_in_zone']
time_in_zone_list

# isolated 0th frame with this name
tiz = time_in_zone_list[0]

for field in tiz:
    print(field.name, ':', field.value)

# disecting all the fields in this frame gives among others a field
# called fields with a list of more instances of the class FieldData
for name in dir(tiz):
    if not name.startswith('_'):
        val = getattr(zones_target, name)
        if callable(val):
            print('method:', name)
        else:
            print('field: ', name, '=', val)


# this list has the following data
for field in tiz.fields:
    print(field.name, ':', field.value)


# this would be the intended way to extract all the values of this frame
tiz.get_field('time_in_hr_zone')
tiz.get_raw_value('time_in_hr_zone')
tiz.get_value('time_in_hr_zone')
tiz.get_value('reference_mesg')

# comparing the 14 differnt frames with name time_in_zone
for frame in time_in_zone_list:
    print(frame.get_value('reference_mesg'), ':', frame.get_value('reference_index'), \
            ':', frame.get_value('time_in_hr_zone'))





# test if record frames are exactly 1 second apart
timestamps = [frame.get_value('timestamp') for frame in data_frames if frame.name == 'record']

for ts in timestamps:
    print(ts.time())

diffs = [b - a for a, b in zip(timestamps, timestamps[1:])]
print(set(diffs))



# sport is also a unique frame in the data

for frame in data_frames:
    if frame.name == 'sport':
        # now I understand that the fields in the frame called sport 
        for field in frame.fields:
            print(field.name, ':', field.value)
        print('\n')


# I could equivalently get the unique frame called sport and do this
sport = next(f for f in data_frames if f.name == 'sport')
sport.get_value('sport')




session = next(f for f in data_frames if f.name == 'session')
for field in session.fields:
    print(field.name, ':', field.value)




#--------------------------------------------------------------------------------
# Intervas API test                                                             #
#--------------------------------------------------------------------------------

import os
import requests
from datetime import date, timedelta
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ["INTERVALS_API_KEY"]
athlete_id = os.environ["INTERVALS_ATHLETE_ID"]

auth = ("API_KEY", api_key)

base_url = f"https://intervals.icu/api/v1/athlete/{athlete_id}"
base_url

oldest = (date.today() - timedelta(days=7)).isoformat()
oldest


resp = requests.get( f"{base_url}/activities", auth=auth, params={"oldest": oldest, "fields": "id"})

resp = requests.get(f"{base_url}/activities", auth=auth, params={"oldest": oldest})
resp.raise_for_status()

print(f"{base_url}/activities")

activities = resp.json()
d = activities[0]
d

for a in activities:
    print(f"{a.get('start_date_local', '')[:10]}  {a.get('id', ''):<12}  {a.get('name', ''):<40}  id={a.get('id')}")

# pick an id from the list above and paste it here
activity_id = activities[0]["id"]
activity_id

fit_resp = requests.get(f"{base_url}/activities/{activity_id}/fit-file", auth=auth)
print(fit_resp.status_code)
print(fit_resp.text)


fit_resp.raise_for_status()

f"{base_url}/activities/{activity_id}/fit-file"


with open(f"{activity_id}.fit", "wb") as f:
    f.write(fit_resp.content)

print(f"saved {activity_id}.fit ({len(fit_resp.content)} bytes)")










