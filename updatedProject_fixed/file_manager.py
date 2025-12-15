import os
import room_manager
import validators

rooms = "data/rooms/rooms.txt"

##Defined addRoom, this asks for an input, gives it the chance to exit, then uppers/strips it and asks for the other variables if it isn't quit. 
# I also added a with/open file read and an if statement to check if the room number being entered already exists in the system. I'm treating it almost like a primary key check
def addRoom():
    roomNum = validators.get_valid_string("Enter the room number to add or type Q to exit: ")
    if roomNum is None:
            return room_manager.Manage_Rooms()
    roomNum = roomNum.strip().upper()
    if roomNum == "Q":
        return room_manager.Manage_Rooms()
    if not roomCheck(roomNum):
        return room_manager.Manage_Rooms()
    # validate capacity input
    while True:
        try:
            roomCapacity = validators.get_valid_int("Enter the room capacity: ")
            break
        except ValueError:
            print("Please enter a valid whole number for capacity.")
    roomType = validators.get_valid_room_type("Enter the room type (e.g., Lecture Hall, Lab, Meeting Room): ")
    if roomType is None:
        return room_manager.Manage_Rooms()
    roomType = roomType.title()
    ##Opens new data file, using the correct file pathing to the file folder. Opens it as infile to use later. 
    # ensure the rooms directory exists so open(..., 'a') won't fail
    rooms_dir = os.path.dirname(rooms)
    if rooms_dir:
        os.makedirs(rooms_dir, exist_ok=True)
    with open(rooms, "a") as outfile:
        outfile.write(f"{roomNum}, {roomCapacity}, {roomType}\n")

def listRooms():
    from room import Room
    try:
        with open(rooms, "r") as infile:
            for line in infile:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(",")
                if len(parts) != 3:
                    continue
                room_obj = Room(parts[0].strip(), parts[1].strip(), parts[2].strip())
                print(room_obj)
    except FileNotFoundError:
        print("File not found.")

def deleteRooms():
    listRooms()
    roomNum = validators.get_valid_int("Enter the room number to delete (or Q to exit): ")
    if roomNum is None:
        return room_manager.Manage_Rooms()
    roomNum = str(roomNum)
    # Check if room exists
    try:
        with open(rooms, "r") as infile:
            room_lines = infile.readlines()
    except FileNotFoundError:
        print("Room file not found.")
        return
    room_found = False
    for line in room_lines:
        if roomNum in line:
            room_found = True
            break
    if not room_found:
        print(f"Room {roomNum} not found.")
        return
    # Check if room has any scheduled events
    events = getEvents()
    ##Checks to see if the event room matches the room number being deleted
    room_has_events = any(event.get_room().strip() == roomNum for event in events)
    if room_has_events:
        print(f"\nCannot delete room {roomNum} — it has scheduled events.")
        return
    # Delete the room
    updated_lines = [line for line in room_lines if roomNum not in line]
    try:
        rooms_dir = os.path.dirname(rooms)
        if rooms_dir:
            os.makedirs(rooms_dir, exist_ok=True)
        with open(rooms, "w") as outfile:
            outfile.writelines(updated_lines)
        print(f"Room {roomNum} deleted successfully.")
    except FileNotFoundError:
        print("File not found.")

def roomCheck(myRoom):
    try:
        with open(rooms, "r") as infile:
            checkRoom = infile.readlines()
            if any(myRoom in line for line in checkRoom):
                print(f"Room {myRoom} already exists.")
                return False
            return True
    except FileNotFoundError:
        print("File not found.")
        return True
    
def eventCheck(myEvent):
    events_file = "data/events/events.txt"
    try:
        with open(events_file, "r") as infile:
            checkEvent = infile.readlines()
            if any(myEvent in line for line in checkEvent):
                print(f"Event {myEvent} already exists.")
                return False
            return True
    except FileNotFoundError:
        print("File not found.")
        return True

##Imports room. Sets path, opens room as append, then creates room_obj object to write to file.
def addRooms(roomNum, roomCapacity, roomType):
    from room import Room
    try:
        rooms_dir = os.path.dirname(rooms)
        if rooms_dir:
            os.makedirs(rooms_dir, exist_ok=True)
        with open(rooms, "a") as outfile:
            room_obj = Room(roomNum, roomCapacity, roomType)
            outfile.write(f"{room_obj.getRoomNumber()},{room_obj.getRoomCapacity()},{room_obj.getRoomType()}\n")
    except FileNotFoundError:
        print("File not found. Creating new file.")    

##Imports event, sets path, opens event as append, then creates event_obj object to write to file.
def addEvents_Manager(room, date, time, attendance, event_type, club, contact):

    from event import Events
    events_file = "data/events/events.txt"
    try:
        events_dir = os.path.dirname(events_file)
        if events_dir:
            os.makedirs(events_dir, exist_ok=True)
        with open(events_file, "a") as outfile:
            event_obj = Events(room, time, attendance, event_type, club, contact)
            outfile.write(f"{event_obj.get_room()},{date},{event_obj.get_time()},{event_obj.get_attendance()},{event_obj.get_event_type()},{event_obj.get_club()},{event_obj.get_contact()}\n")
    except FileNotFoundError:
        print("File not found. Creating new file.")

def getRooms():

    from room import Room
    rooms_list = []
    try:
        with open(rooms, "r") as infile:
            for line in infile:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(",")
                # expect exactly 3 parts (name,capacity,type)
                if len(parts) != 3:
                    continue
                room_obj = Room(parts[0].strip(), parts[1].strip(), parts[2].strip())
                rooms_list.append(room_obj)
    except FileNotFoundError:
        # No rooms yet — return empty list rather than crashing
        return []
    return rooms_list

def getEvents():
    from event import Events
    events = []
    events_file = "data/events/events.txt"
    try:
        with open(events_file, "r") as infile:
            for line in infile:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(",")
                # expect exactly 7 parts (room,date,time,attendance,event_type,club,contact)
                if len(parts) != 7:
                    continue
                event_obj = Events(parts[0].strip(), parts[2].strip(), parts[3].strip(), parts[4].strip(), parts[5].strip(), parts[6].strip())
                # Attach date as an attribute for compatibility
                event_obj.get_date = lambda d=parts[1].strip(): d
                events.append(event_obj)
    except FileNotFoundError:
        # No events yet — return empty list rather than crashing
        return []
    return events

def deleteEvents():

    events = getEvents()
    if not events:
        print("No events to delete.")
        return

    # Display current events
    print("\nCurrent Events:")
    for i, evt in enumerate(events):
        if hasattr(evt, 'get_room'):
            print(f"{i+1}. Room: {evt.get_room()} || Date: {evt.get_date()} || Time: {evt.get_time()} || Club: {evt.get_club()}")
        else:
            print(f"{i+1}. Room: {evt['room']} || Date: {evt['date']} || Time: {evt['time']} || Club: {evt['club']}")

    with open(rooms, "r") as infile:
        for lines in infile:
            print(lines.strip())

    ##Prevents invalid string inputs other than q from working, and allows only valid existing room numbers
    while True:
        room = validators.get_valid_string("Enter room of event to delete (or Q to exit): ")
        if room is None:
            return
        room = room.strip().upper()
        if room == "Q":
            return
        if room:
            break
        print("Invalid input. Please enter a valid room or Q to exit.")

    #Prevents invalid string inputs other than q from working, and allows only valid date formats
    while True:
        date = validators.get_valid_date("Enter date of event to delete (YYYY-MM-DD) or Q to exit: ")
        if date is None:
            return
        date = date.strip()
        if date.upper() == "Q":
            return
        if date:
            break
        print("Invalid input. Please enter a valid date or Q to exit.")

    # Prevents invalid string inputs other than q from working, and allows only valid hour formats
    while True:
        time = validators.get_valid_string("Enter time of event to delete (HH:MM-HH:MM) or Q to exit: ")
        if time is None:
            return
        time = time.strip()
        if time.upper() == "Q":
            return
        if time:
            break
        print("Invalid input. Please enter a valid time or Q to exit.")

    # Filter out the matching event
    updated_events = [evt for evt in events if not ((evt.get_room() if hasattr(evt, 'get_room') else evt['room']) == room and (evt.get_date() if hasattr(evt, 'get_date') else evt['date']) == date and (evt.get_time() if hasattr(evt, 'get_time') else evt['time']) == time)]

    if len(updated_events) == len(events):
        print(f"No event found for room {room} on {date} at time {time}.")
        return

    # Write updated events back to file (with date)
    events_file = "data/events/events.txt"
    try:
        events_dir = os.path.dirname(events_file)
        if events_dir:
            os.makedirs(events_dir, exist_ok=True)
        with open(events_file, "w") as outfile:
            for evt in updated_events:
                if hasattr(evt, 'get_room'):
                    outfile.write(f"{evt.get_room()} || {evt.get_date()} || {evt.get_time()} || {evt.get_attendance()} || {evt.get_event_type()} || {evt.get_club()} || {evt.get_contact()}\n")
                else:
                    outfile.write(f"{evt['room']} || {evt['date']} || {evt['time']} || {evt['attendance']} || {evt['event_type']} || {evt['club']} || {evt['contact']}\n")
        print(f"Event deleted successfully.")
    except FileNotFoundError:
        print("File not found.")


def save_events_report(date_str, events_list, folder="reports/eventsfordate"):
    
    reports_dir = os.path.normpath(folder)
    os.makedirs(reports_dir, exist_ok=True)
    report_path = os.path.join(reports_dir, f"{date_str}.txt")
    with open(report_path, "w", encoding="utf-8") as rf:
        rf.write(f"Events for {date_str} (sorted by room):\n")
        for evt in events_list:
            if hasattr(evt, 'get_room'):
                rf.write(f"Room: {evt.get_room()} || Time: {evt.get_time()} || Attendance: {evt.get_attendance()} || Type: {evt.get_event_type()} || Club: {evt.get_club()} || Contact: {evt.get_contact()}\n")
            else:
                rf.write(f"Room: {evt['room']} || Time: {evt['time']} || Attendance: {evt['attendance']} || Type: {evt['event_type']} || Club: {evt['club']} || Contact: {evt['contact']}\n")
    return report_path

