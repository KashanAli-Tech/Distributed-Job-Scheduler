from datetime import datetime

events = []

# to add an event to the list
def add_event(message, level="INFO"):

    events.append(
        {
            "message": message,
            "level": level,
            "timestamp": datetime.now().strftime("%H:%M:%S") 
        }
    )

# to print the list of events
def get_events():

    return events[-50:]

