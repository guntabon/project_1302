#Creating events class
class Events: 
    #defining events data
    def __init__(self, room, time, attendance, event_type, club, contact):
        self.__room = room

        self.__time = time

        self.__attendance = attendance

        self.__event_type = event_type

        self.__club = club

        self.__contact = contact

#defining set methods for events data
    def set_room(self, room):
        self.__room = room

    def set_time(self, time):
        self.__time = time
    
    def set_attendance(self, attendance):
        self.__attendance = attendance
    
    def set_event_type(self, event_type):
        self.__event_type = event_type  

    def set_club(self, club):
        self.__club = club

    def set_contact(self, contact):
        self.__contact = contact    

 #defining get methods for events data

    def get_room(self):
        return self.__room
    
    def get_time(self):
        return self.__time  
    
    def get_attendance(self):
        return self.__attendance
    
    def get_event_type(self):
        return self.__event_type    
    
    def get_club(self):
        return self.__club
    
    def get_contact(self):
        return self.__contact
    
    

        