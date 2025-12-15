def get_valid_room_type(prompt):
    while True:
        user_input = input(prompt).strip()
        if user_input.upper() == "Q":
            return
        if isinstance(user_input, str) and user_input.strip():
            return user_input
        print("Invalid input. Please enter a non-empty string or Q to quit.")
from datetime import datetime
def get_valid_int(prompt):
    while True:
        user_input = input(prompt).upper().strip()
        if user_input == "Q":
            return
        try:
            return int(user_input)
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def get_valid_float(prompt):
    while True:
        user_input = input(prompt).upper().strip()
        if user_input == "Q":
            return
        try:
            return float(user_input)
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def get_valid_string(prompt):
    while True:
        user_input = input(prompt).strip()
        if user_input.upper() == "Q":
            return
        if user_input:
            return user_input
        print("Invalid input. Please enter a valid input or Q to quit.")
        
def get_valid_date(prompt):
    while True:
        user_input = input(prompt).upper().strip()
        if user_input == "Q":
            return
        try:
            datetime.strptime(user_input, "%Y-%m-%d")
            return user_input
        except ValueError:
            print("Invalid date format. Please enter a date in YYYY-MM-DD format.")
def get_valid_time(prompt):
    while True:
        user_input = input(prompt).upper().strip()
        if user_input == "Q":
            return
        try:
            # Expecting format HH:MM-HH:MM
            start_str, end_str = user_input.split("-")
            start = datetime.strptime(start_str.strip(), "%H:%M")
            end = datetime.strptime(end_str.strip(), "%H:%M")
            if end <= start:
                print("End time must be after start time.")
                continue
            return user_input
        except Exception:
            print("Invalid time range format. Please enter a range in HH:MM-HH:MM format.")

            ##Makes sure time is correctly formatted
def parse_time_range(time_range):
    start_str, end_str = time_range.split('-')
    start = datetime.strptime(start_str.strip(), "%H:%M")
    end = datetime.strptime(end_str.strip(), "%H:%M")
    return start, end

##Makes sure no time conflicts exist
def checkTime(new_room, new_date, new_time, existing_events):
    try:
        new_start, new_end = parse_time_range(new_time)
    except Exception:
        return "invalid"
    for evt in existing_events:
        try:
            evt_room = evt.get_room() if hasattr(evt, 'get_room') else evt["room"]
            evt_date = evt.get_date() if hasattr(evt, 'get_date') else evt["date"]
            if evt_room != new_room or evt_date != new_date:
                continue
            existing_time = evt.get_time() if hasattr(evt, 'get_time') else evt["time"]
            existing_start, existing_end = parse_time_range(existing_time)
            if new_start < existing_end and new_end > existing_start:
                return True
        except Exception:
            continue

    return False 
