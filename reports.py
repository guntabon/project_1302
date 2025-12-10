
import os
import file_manager
from datetime import datetime
import menu


def events_for_date(date_str):
	"""Print all events for `date_str` (YYYY-MM-DD) sorted by room and write report file.

	Creates `reports/eventsfordate/{date_str}.txt` containing the same output.

	Returns the list of events for that date (each is a dict).
	"""
	# validate date
	try:
		datetime.strptime(date_str, "%Y-%m-%d")
	except Exception:
		print("Invalid date format. Expected YYYY-MM-DD.")
		return []

	events = file_manager.getEvents()
	# filter by date
	events_for_day = [e for e in events if e.get("date") == date_str]

	if not events_for_day:
		print(f"No events found for {date_str}.")
		return []

	# sort by room (lexicographically) then by time
	events_for_day.sort(key=lambda e: (e.get("room", ""), e.get("time", "")))

	# Print to console
	print(f"Events for {date_str} (sorted by room):")
	for evt in events_for_day:
		print(f"Room: {evt['room']}, Time: {evt['time']}, Attendance: {evt['attendance']}, Type: {evt['event_type']}, Club: {evt['club']}, Contact: {evt['contact']}")


	# Save the report using file_manager helper
	try:
		report_path = file_manager.save_events_report(date_str, events_for_day)
		print(f"Report saved to {report_path}")
	except Exception as e:
		print(f"Failed to write report: {e}")

	return events_for_day
def events_by_room():
	rooms = file_manager.getRooms()
	events = file_manager.getEvents()
	if not rooms:
		print("No rooms found.")
		return
	for room in rooms:
		room_name = room.get("name")
		print(f"\nEvents for Room: {room_name}")
		room_events = [e for e in events if e.get("room") == room_name]
		if not room_events:
			print("  No events scheduled.")
			continue
		# Sort events by date and time
		room_events.sort(key=lambda e: (e.get("date", ""), e.get("time", "")))
		for evt in room_events:
			print(f"  Date: {evt['date']}, Time: {evt['time']}, Attendance: {evt['attendance']}, Type: {evt['event_type']}, Club: {evt['club']}, Contact: {evt['contact']}")

def Report_manager():
    whileTrue = True
    while whileTrue:
        print("\n1. View reports for all rooms: ")
        print("2. Generate Events Report for a Date: ")
        print("3. View Events by Room: ")
        print("4. Go back to main menu")
        userinput = int(input("Select an option 1-4: "))
        match userinput:
            case 1:
                all_rooms()
            case 2:
                date_str = input("Enter date (YYYY-MM-DD): ").strip()
                events_for_date(date_str)
            case 3:
                events_by_room()
                
            case 4:
                menu.Menu()
                