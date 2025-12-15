
import event_manager
import room_manager
import validators
import reports

##Menu program
def Menu():
    ##While loop to control
    whiletrue = True
    while whiletrue:
           
        # create a label for the menu with lines and a title
        print("\n" + "="*32)
        print("Room and Event Management System")
        print("="*32)
        print("1. Manage Rooms")
        print("2. Manage Events")
        print("3. Reports")
        print("4. Exit")
        userinput = validators.get_valid_int("Please choose an option 1-4: ")
        if userinput is None:
            whiletrue = False
            break
        match userinput:
            case 1:
                room_manager.Manage_Rooms()
            case 2:
                event_manager.Manage_Events()
            case 3:
                reports.Report_manager()
            case 4:
                whiletrue = False
            case 4:

                whiletrue = False



                
