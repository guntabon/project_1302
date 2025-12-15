##Imported room, validators and menu to reference between menus.
import validators
import file_manager

##While loop control variable
whiletrue = True

 ## STILL NEEDS TO BE WRITTEN       
def cancelRoomTime():
    print("")

def Manage_Rooms():
    whileTrue = True
    while whileTrue:
        print("\n" + "="*20)
        print("Room Management Menu")
        print("="*20)
        print("1. Add a Room")
        print("2. List all Rooms")
        print("3. Delete Unused Room")
        print("4. Go back to main menu")
        userinput = validators.get_valid_int("\nSelect an option 1-4: ")
        match userinput:
            case 1:
                file_manager.addRoom()
            case 2:
                file_manager.listRooms()
            case 3:
                file_manager.deleteRooms()
            case 4:
                return
            