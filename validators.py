# validate user input data as integer data type
def CheckInt(myVal):
    try:
        val = int(myVal)
        return True
    except ValueError:
        return False