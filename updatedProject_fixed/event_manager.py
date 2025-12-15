import file_manager
import validators
from datetime import datetime


##Adds event if no conflicts exist
def addEvent(room, date, time, attendance, event_type, club, contact):
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except Exception:
        print("Invalid date format. Expected YYYY-MM-DD. Event not added.")
        return
    # Check room capacity
    ##Stores rooms in rooms variable
    rooms = file_manager.getRooms()
    ##Room_obj finds the room that matches the input room
    room_obj = next((r for r in rooms if r.getRoomNumber().strip().upper() == room.strip().upper()), None)
    ##IF room doesnt exist, print message and exit function
    if not room_obj:
        print(f"Room '{room}' not found. Event not added.")
        return
    try:
        ##Try to get room capacity
        capacity = int(room_obj.getRoomCapacity())
    except Exception:
        ##Prints invalid room capacity if not an integer 
        print(f"Invalid room capacity for room '{room}'. Event not added.")
        return
    if attendance > capacity:
        ##Greater than check to see if attendance > capacity
        print(f"Warning: Attendance ({attendance}) exceeds room capacity ({capacity}). Event not added.")
        return
    existing_events = file_manager.getEvents()
    result = validators.checkTime(room, date, time, existing_events)
    if result == "invalid":
        print("Invalid time format. Expected HH:MM-HH:MM. Event not added.")
        return
    if result is True:
        print("Cannot add event — room is booked at that date/time. Event not added.")
        return
    file_manager.addEvents_Manager(room, date, time, attendance, event_type, club, contact)
    print("Event added successfully.")

##Event manager menu 
def Manage_Events():
    whileTrue = True
    while whileTrue:
        print("\n" + "="*21)
        print("Event Management Menu")
        print("="*21)
        print("\n1. Add an Event")
        print("2. List all Events")
        print("3. Delete an Event")
        print("4. Go back to main menu")
        userinput = validators.get_valid_int("Select an option 1-4: ")
        match userinput:
            case 1:
                room = validators.get_valid_string("Enter room for the event (or Q to exit): ")
                if room is None:
                    return
                room = room.strip()
                if room.upper() == "Q":
                    return
                date = validators.get_valid_date("Please choose a valid date: ")
                time = validators.get_valid_time("Please choose a valid time (HH:MM-HH:MM): ")
                attendance = validators.get_valid_int("Enter expected attendance: ")
                event_type = validators.get_valid_string("Enter event type: ")
                club = validators.get_valid_string("Enter club name: ")
                contact = validators.get_valid_string("Enter contact information: ")
                addEvent(room, date, time, attendance, event_type, club, contact)
            case 2:
                events = file_manager.getEvents()
                if events:
                    for evt in events:
                        if hasattr(evt, 'get_room'):
                            print(f"Room: {evt.get_room()} || Date: {evt.get_date()} || Time: {evt.get_time()} || Attendance: {evt.get_attendance()} || Type: {evt.get_event_type()} || Club: {evt.get_club()} || Contact: {evt.get_contact()}")
                        else:
                            print(f"Room: {evt['room']} || Date: {evt.get('date','')} || Time: {evt['time']} || Attendance: {evt['attendance']} || Type: {evt['event_type']} || Club: {evt['club']} || Contact: {evt['contact']}")
                else:
                    print("No events scheduled.")
            
            case 3:
                file_manager.deleteEvents()
            case 4:
                return
