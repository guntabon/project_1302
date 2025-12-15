
import os
import file_manager
from datetime import datetime
import validators


def events_for_date(date_str):
    # validate date
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except Exception:
        print("Invalid date format. Expected YYYY-MM-DD.")
        return []
    events = file_manager.getEvents()
    # filter by date (using get_date method if available)
    events_for_day = [e for e in events if (e.get_date() if hasattr(e, 'get_date') else None) == date_str]

    if not events_for_day:
        print(f"No events found for {date_str}.")
        return []

    # sort by room (lexicographically) then by time
    events_for_day.sort(key=lambda e: (e.get_room() if hasattr(e, 'get_room') else '', e.get_time() if hasattr(e, 'get_time') else ''))

    # Print to console
    print(f"Events for {date_str} (sorted by date):")
    for evt in events_for_day:
        if hasattr(evt, 'get_room'):
            print(f"\nRoom: {evt.get_room()} || Time: {evt.get_time()} || Attendance: {evt.get_attendance()} || Type: {evt.get_event_type()} || Club: {evt.get_club()} || Contact: {evt.get_contact()}")
        else:
            print(f"\nRoom: {evt['room']} || Time: {evt['time']} || Attendance: {evt['attendance']} || Type: {evt['event_type']} || Club: {evt['club']} || Contact: {evt['contact']}")

    # Save the report using file_manager helper
    try:
        report_path = file_manager.save_events_report(date_str, events_for_day)
        print(f"Report saved to {report_path}")
    except Exception as e:
        print(f"Failed to write report: {e}")

    return events_for_day


def all_rooms():
    """Group all events by room, print them, and save a rooms report.

    Writes the report to `reports/roomsreport/roomsreport.txt` and returns the path.
    """
    events = file_manager.getEvents()
    if not events:
        print("No events found to include in rooms report.")
        return None

    from collections import defaultdict
    rooms_map = defaultdict(list)
    for evt in events:
        room_name = evt.get_room() if hasattr(evt, 'get_room') else evt['room']
        rooms_map[room_name].append(evt)

    # ensure directory exists
    report_dir = os.path.join("reports", "roomsreport")
    os.makedirs(report_dir, exist_ok=True)
    report_path = os.path.join(report_dir, "roomsreport.txt")

    # write report grouped by room
    with open(report_path, "w", encoding="utf-8") as rf:
        from file_manager import getRooms
        room_objs = getRooms()
        room_capacity_map = {room.getRoomNumber(): room.getRoomCapacity() for room in room_objs}
        for room_name in sorted(rooms_map.keys()):
            capacity = room_capacity_map.get(room_name, 'Unknown')
            rf.write(f"Room: {room_name} || Capacity: {capacity}\n")
            # sort events for this room by date then time
            rooms_map[room_name].sort(key=lambda x: (x.get_date() if hasattr(x, 'get_date') else '', x.get_time() if hasattr(x, 'get_time') else ''))
            for evt in rooms_map[room_name]:
                if hasattr(evt, 'get_date'):
                    rf.write(
                        f"  Date: {evt.get_date()} || Time: {evt.get_time()} || Attendance: {evt.get_attendance()} || Type: {evt.get_event_type()} || Club: {evt.get_club()} || Contact: {evt.get_contact()}\n"
                    )
                else:
                    rf.write(
                        f"  Date: {evt['date']} || Time: {evt['time']} || Attendance: {evt['attendance']} || Type: {evt['event_type']} || Club: {evt['club']} || Contact: {evt['contact']}\n"
                    )
            rf.write("\n")
    with open(report_path, "r", encoding="utf-8") as rf:
        print((rf.read()))

    print(f"Rooms report saved to {report_path}")
    return report_path

def events_by_room():
    rooms = file_manager.getRooms()
    events = file_manager.getEvents()
    if not rooms:
        print("No rooms found.")
        return
    print("Available rooms:")
    # Sort rooms by room number (as integer if possible)
    def room_sort_key(room):
        try:
            return int(room.getRoomNumber() if hasattr(room, 'getRoomNumber') else room['name'])
        except Exception:
            return room.getRoomNumber() if hasattr(room, 'getRoomNumber') else room['name']
    for room in sorted(rooms, key=room_sort_key):
        if hasattr(room, 'getRoomNumber'):
            print(f"  Room {room.getRoomNumber()} (Capacity: {room.getRoomCapacity()}, Type: {room.getRoomType()})")
        else:
            print(f"  Room {room['name']} (Capacity: {room['capacity']}, Type: {room['type']})")
    while True:
        selected = input("Enter the room number to view events for (or Q to exit): ").strip()
        if selected.upper() == "Q":
            return
        if selected.isdigit():
            break
        print("Invalid input. Please enter a numeric room number or Q to exit.")
    room_events = [e for e in events if str(e.get_room() if hasattr(e, 'get_room') else e['room']) == selected]
    output_lines = []
    output_lines.append(f"Events for Room: {selected}\n")
    if not room_events:
        output_lines.append("  No events scheduled.\n")
        print(''.join(output_lines))
        # Write to file
        os.makedirs(os.path.join("reports", "eventsbyroom"), exist_ok=True)
        file_path = os.path.join("reports", "eventsbyroom", f"{selected}.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(output_lines)
        print(f"Report saved to {file_path}")
        return
    # Sort events by date and time
    room_events.sort(key=lambda e: (e.get_date() if hasattr(e, 'get_date') else '', e.get_time() if hasattr(e, 'get_time') else ''))
    for evt in room_events:
        if hasattr(evt, 'get_date'):
            line = f"  Date: {evt.get_date()} || Time: {evt.get_time()} || Attendance: {evt.get_attendance()} || Type: {evt.get_event_type()} || Club: {evt.get_club()} || Contact: {evt.get_contact()}\n"
        else:
            line = f"  Date: {evt['date']} || Time: {evt['time']} || Attendance: {evt['attendance']} || Type: {evt['event_type']} || Club: {evt['club']} || Contact: {evt['contact']}\n"
        output_lines.append(line)
    print(''.join(output_lines))
    # Write to file
    os.makedirs(os.path.join("reports", "eventsbyroom"), exist_ok=True)
    file_path = os.path.join("reports", "eventsbyroom", f"{selected}.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(output_lines)
    print(f"Report saved to {file_path}")

def Report_manager():
    whileTrue = True
    while whileTrue:
        print("\n1. View reports for all rooms: ")
        print("2. Generate Events Report for a Date: ")
        print("3. View Events by Room: ")
        print("4. Go back to main menu")
        userinput = validators.get_valid_int("\nSelect an option 1-4: ")
        match userinput:
            case 1:
                all_rooms()
            case 2:
                date_str = input("Enter date (YYYY-MM-DD): ").strip()
                events_for_date(date_str)
            case 3:
                events_by_room()
            case 4:
                return