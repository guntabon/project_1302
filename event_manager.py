import event
import file_manager

def addEvent(room, time, attendance, event_type, club, contact):
    file_manager.addEvents(room, time, attendance, event_type, club, contact)

from datetime import datetime

def parse_time_range(time_range):
    start_str, end_str = time_range.split('-')
    start = datetime.strptime(start_str.strip(), "%H:%M")
    end = datetime.strptime(end_str.strip(), "%H:%M")
    return start, end

def checkTime(new_room, new_time, existing_events):
     new_start, new_end = parse_time_range(new_time)
    
    for event in existing_events:
        room = event["room"]
        if room != new_room:
            continue  # Skip events in other rooms

        existing_start, existing_end = parse_time_range(event["time"])

        # Check if time ranges overlap
        if new_start < existing_end and new_end > existing_start:
            return True  # Overlap found
    
    return False  # No overlaps
    
def addEvent(room, time, attendance, event_type, club, contact):
    existing_events = file_manager.getEvents()  # assume this reads from file
    if checkTime(room, time, existing_events):
        print(" Cannot add event — time overlaps with an existing one.")
        return
    else:
        file_manager.addEvents(room, time, attendance, event_type, club, contact)
        print(" Event added successfully.")

  
    #    if __name__ == "__main__":
    #events = [
    #    {"room": "A", "time": "10:00-12:00"},
    #    {"room": "A", "time": "13:00-14:00"}, ]
    

    #new_event = ("A", "11:30-12:30")
   #overlap = checkTime(new_event[0], new_event[1], events)

    #if overlap:
    #    print("Times overlap!")
    #else:
    #    print("No overlap!")