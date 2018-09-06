import inspect

VDM_NEWLINE = "\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t"
ONE_OBJ_NEWLINE = "\n\t\t\t\t\t\t\t\t\t\t\t\t"

def bit(value, msb, lsb):
    if msb < lsb:
        print("msb < lsb")
        return -1
    return (value >> lsb) & ((1 << (msb - lsb + 1)) - 1)

def checkRSV0(value, msb, lsb, msg="Shall be set to 0 and shall be ignored"):
    if bit(value, msb, lsb) != 0:
        print("{}, B{}..{}, {}".format(inspect.stack()[1][3], msb, lsb, msg))
