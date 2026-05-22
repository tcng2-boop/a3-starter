# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Tiffany Ng
# Tcng2@uci.edu
# 52892812


import json
import socket
import time
import ds_protocol

def send(server:str, port:int, username:str, password:str, message:str, bio:str=None):
  '''
  The send function joins a ds server and sends a message, bio, or both

  :param server: The ip address for the ICS 32 DS server.
  :param port: The port where the ICS 32 DS server is accepting connections.
  :param username: The user name to be assigned to the message.
  :param password: The password associated with the username.
  :param message: The message to be sent to the server.
  :param bio: Optional, a bio for the user.
  '''
  #TODO: #return either True or False depending on results of required operation
  try:
      client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      client.connect((server, port))
      send_stream = client.makefile("w")
      recv_stream = client.makefile("r")

      join_message = json.dumps({
        "join": {
          "username": username,
          "password": password,
          "token": ""
        }
      })
      send_stream.write(join_message + "\n")
      send_stream.flush()

      response = recv_stream.readline()
      
      response_data = ds_protocol.extract_json(response)
      

      if response_data.type != "ok":
        client.close()
        return False
      
      token = response_data.token
      

      post_message = json.dumps({
        "token": token,
        "post": {
          "entry": message,
          "timestamp": str(time.time())
        }
      })

      send_stream.write(post_message + "\n")
      send_stream.flush()

      post_response = recv_stream.readline()
      
      post_response_data = ds_protocol.extract_json(post_response)
      

      if post_response_data.type != "ok":
        client.close()
        return False
      if bio is not None:
        bio_message = json.dumps({
            "token": token,
            "bio": {
                "entry": bio,
                "timestamp": str(time.time())
            }
        })

        send_stream.write(bio_message + "\n")
        send_stream.flush()

        bio_response = recv_stream.readline()
        #print("DEBUG bio response:", bio_response)  # add this
        bio_response_data = ds_protocol.extract_json(bio_response)
        #print("DEBUG bio type:", bio_response_data.type)  # add this

        if bio_response_data.type != "ok":
          client.close()
          return False
    
      client.close()
      return True

  except Exception:
      return False
  
    
    
