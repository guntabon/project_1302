# define the class Room
class Room:
    # initialize the Room with a name and description
    def __init__(self, roomNumber, roomCapacity, roomType):
        self.__roomNumber = roomNumber
        self.__roomCapacity = roomCapacity
        self.__roomType = roomType


    # setters for each attribute
    def setRoomNumber(self, roomNumber):
        self.__roomNumber = roomNumber
    
    def setRoomCapacity(self, roomCapacity):
        self.__roomCapacity = roomCapacity

    def setRoomType(self, roomType):
        self.__roomType = roomType


    # getters for each attribute
    def getRoomNumber(self):
        return self.__roomNumber

    def getRoomCapacity(self):
        return self.__roomCapacity

    def getRoomType(self):
        return self.__roomType

    
    # represent the Room object as a string
    def __str__(self):
        return f"Room Number: {self.__roomNumber} || Capacity: {self.__roomCapacity} || Type: {self.__roomType}\n"