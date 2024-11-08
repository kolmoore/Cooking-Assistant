import json

filepath = "/Users/kollinmoore/Documents/GitHub/HCI584/Project/system_messages.json"

def save(new_key,new_message):

    with open(filepath, "r+") as f:
        try:
            current = json.load(f)
            current[new_key] = new_message
            updated = current
            f.seek(0)

        except:
            updated = {new_key:new_message}

        json.dump(updated, f, indent =4)
        return(updated)


def load(key):
    with open(filepath, "r") as f:
        current = json.load(f)
        return(current[key])
    


def keys():
    with open(filepath, "r+") as f:
        current = json.load(f)
        return(current.keys())
    

def delete(key):
    with open(filepath, "r+") as f:
        try:
            current = json.load(f)
        except:
            return("No messages have been loaded")
        
        try:
            del current[key]
            updated = current
            f.seek(0)
            json.dump(updated, f, indent =4)
            f.truncate()
        except:
            return("That key already doesn't exist")
        return(current.keys())