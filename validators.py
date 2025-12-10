# validate user input data as integer data type
def CheckInt(myVal):
    try:
        val = int(myVal)
        return True
    except ValueError:
        return False
    
    # validate user input data as string data type
def CheckStr(myVal):
    try:
        val = str(myVal)
        return True
    except ValueError:
        return False