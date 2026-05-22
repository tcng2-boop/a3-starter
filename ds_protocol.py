# ds_protocol.py

# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Tiffany Ng
# tcng2@uci.edu
# 52892812

import json
from collections import namedtuple

# Namedtuple to hold the values retrieved from json messages.
# TODO: update this named tuple to use DSP protocol keys

DataTuple = DataTuple = namedtuple(
    'DataTuple',
    ['type', 'message', 'token']
)

def extract_json(json_msg:str) -> DataTuple:
  '''
  Call the json.loads function on a json string and convert it to a DataTuple object
  
  TODO: replace the pseudo placeholder keys with actual DSP protocol keys
  '''
  try:
    response = json.loads(json_msg)
    json_obj = response["response"]
    response_type = json_msg["type"]
    message = json_msg["message"]
    token = json_msg.get("token", "")
  except json.JSONDecodeError:
    print("Json cannot be decoded.")

  return DataTuple(
            response_type,
            message,
            token
        )
